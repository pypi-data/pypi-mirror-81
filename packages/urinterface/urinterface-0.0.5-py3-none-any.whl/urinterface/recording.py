import logging
import os
import sys
from queue import Queue

from third_party.rtde import rtde_config, csv_writer, rtde

STOP_REQUEST = 1

def _start_recording(rtde_con, config_file, frequency, log):
    # Connect to RTDE
    rtde_con.connect()

    # get controller version
    rtde_con.get_controller_version()

    # check existence of config file
    if not os.path.isfile(config_file):
        msg = f"Config file does not exists. Expected to find it in {config_file}. Current working dir is {os.getcwd()}."
        log.error(msg)
        sys.exit(1)

    conf = rtde_config.ConfigFile(config_file)
    output_names, output_types = conf.get_recipe('out')

    # setup recipes
    if not rtde_con.send_output_setup(output_names, output_types, frequency=frequency):
        log.error('Unable to configure output')
        sys.exit(1)

    # start data synchronization
    if not rtde_con.send_start():
        log.error('Unable to start synchronization')
        sys.exit(1)

    return rtde_con, output_names, output_types


def _read_csv_stream(filename, samples, output_names, output_types, read_row_function, _thread_log):
    write_mode = 'w'

    with open(filename, write_mode) as csvfile:
        writer = csv_writer.CSVWriter(csvfile, output_names, output_types)

        writer.writeheader()

        i = 1
        keep_running = True
        while keep_running:

            if samples > 0:
                _thread_log.debug("{:.2%} done.".format(float(i) / float(samples)))
            else:
                _thread_log.debug("{:3d} samples.".format(i))

            state, should_continue = read_row_function()
            _thread_log.debug(f"Sample received: {state}")
            if samples>0:
                keep_running = i < samples
            else:
                keep_running = should_continue

            writer.writerow(state)
            i += 1


def _recording_thread(rtde_con, config_file, filename, frequency, samples, communication_queue: Queue):
    _thread_log = logging.getLogger("Recording")

    rtde_con, output_names, output_types = _start_recording(rtde_con, config_file, frequency, _thread_log)

    def read_row_function():
        try:
            state = rtde_con.receive(binary=False)
            assert state is not None, state
        except rtde.RTDEException:
            _thread_log.error("Disconnected")
            rtde_con.disconnect()
            sys.exit(1)
        # Check if logging should be stopped.
        # This does not lead to race conditions because of Python's GIL
        keep_running = communication_queue.qsize() == 0

        if not keep_running:
            signal = communication_queue.get_nowait()
            assert signal == STOP_REQUEST, f"Strange signal received: {signal}."
            _thread_log.info("Stop record signal received.")

        return state, keep_running

    _read_csv_stream(filename, samples, output_names, output_types, read_row_function, _thread_log)

    rtde_con.send_pause()
    rtde_con.disconnect()
