#!/usr/bin/python3

from time import time, sleep
import argparse

def serial_read(device_path, delay=0.5, file_path=None):
    reader = HMReader(device_path)

    if file_path is not None:
        with open(file_path, 'w') as f:
            f.write('serial_data\n')

    while True:
        timestamp = time()
        ret = reader.read()

        if file_path is not None:
            with open(file_path, 'a') as f:
                f.write('%f %.8f %.8f %.8f\n' % (timestamp,
                    ret['Current'], ret['Voltage'], ret['Power']))

        print('\x1b[1K\r%.6fA %.6fV %.6fW' % (ret['Current'],
            ret['Voltage'], ret['Power']), end='')
        sleep(delay)

    reader.close()


def serial_plot(device_path, delay=0.5, file_path=None):
    reader = HMReader(device_path)
    time_list, power_list = list(), list()

    if file_path is not None:
        with open(file_path, 'w') as f:
            f.write('serial_data\n')

    def anim(i):
        timestamp = time()
        ret = reader.read()

        if file_path is not None:
            with open(file_path, 'a') as f:
                f.write('%f %.8f %.8f %.8f\n' % (timestamp,
                    ret['Current'], ret['Voltage'], ret['Power']))

        time_list.append(timestamp)
        power_list.append(ret['Power'])

        ax.clear()
        plt.xlabel('t')
        plt.ylabel('W')
        ax.relim()
        ax.autoscale()
        ax.plot(time_list, power_list)
        ax.set_ylim(bottom=0)

    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig, anim, interval=(delay*1000))
    plt.show()

    reader.close()



def plot(file_paths):
    serial_data, inf_data = list(), list()
    for path in file_paths:
        with open(path, 'r') as f:
            lines = f.readlines()
            if 'serial_data' in lines[0]:
                time_list, current_list, voltage_list, power_list = list(), list(), list(), list()
                for line in lines[1:]:
                    line_args = line.split()
                    if len(line_args) == 4:
                        try:
                            time = float(line_args[0])
                            current = float(line_args[1])
                            voltage = float(line_args[2])
                            power = float(line_args[3])
#                            if current < 0 or voltage < 4.5 or voltage > 5.5:
#                                continue
                            time_list.append(time)
                            current_list.append(current)
                            voltage_list.append(voltage)
                            power_list.append(power)
                        except ValueError:
                            pass
                serial_data.append((time_list, current_list, voltage_list, power_list))
            elif 'label_data' in lines[0]:
                data_list = list()
                for line in lines[1:]:
                    line_args = line.split()
                    if len(line_args) == 2:
                        try:
                            time = float(line_args[0])
                            data_list.append((time, line_args[1]))
                        except ValueError:
                            pass
                inf_data.append(data_list)

    fig, ax = plt.subplots()
    plt.xlabel('t')
    plt.ylabel('W')
    for (time_list, current_list, voltage_list, power_list) in serial_data:
        plt.plot(time_list, power_list)
    for data_list in inf_data:
        for (time, label) in data_list:
            plt.axvline(time, color='darksalmon')
            plt.text(time, 1, label, rotation=45, transform=ax.get_xaxis_transform())

    plt.ylim(bottom=0)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Power measuring tool to use with 10 bit serial UART output values of a microcontroller with ACS712 5A")
    subparsers = parser.add_subparsers(dest='cmd')
    monitorparser = subparsers.add_parser('monitor', help='Monitor given device for serial input')
    monitorparser.add_argument('device_path', type=str, help='Path to serial device from which analog input data is read')
    monitorparser.add_argument('-i', '--interval',  type=float, default=0.5, help='Writing interval of average current that is measured')
    monitorparser.add_argument('-f', '--file', help='Write data to file with given path')
    monitorparser.add_argument('-l', '--live', action='store_true', default=False, help='Plot live graph instead of command line output')
    monitorparser.add_argument('-p', '--power', action='store_true', default=False, help='Plot live graph instead of command line output')
    #monitorparser.add_argument('-m', '--measured_device', help='Receive serial signals from measured device with given device path')
    plotparser = subparsers.add_parser('plot', help='Create plot from file paths')
    plotparser.add_argument('file_paths', nargs='+', help='path to data files')
    args = parser.parse_args()

    if args.cmd == 'plot':
        import matplotlib.pyplot as plt
        from matplotlib import axes
 
        plot(args.file_paths)
    elif args.cmd == 'monitor':
        from hm310p import HMReader
        from serial import Serial

        if args.live:
            import matplotlib.pyplot as plt
            from matplotlib import axes
            import matplotlib.animation as animation

            serial_plot(args.device_path, args.interval, args.file)
        else:
            serial_read(args.device_path, args.interval, args.file)
