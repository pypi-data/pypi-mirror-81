import argparse

from SGCC.savgol import get_coefficients


def get_arguments():
    parser = argparse.ArgumentParser(description='Generate Savitsky-Golay filter coefficients for different parameters.')

    parser.add_argument('-ws', '--window_size',
                        help='Window size of the filter',
                        required=True, type=int)
    parser.add_argument('-o', '--order',
                        help='Order of the fit of the filter',
                        required=False, default=1, type=int)
    parser.add_argument('-s', '--smoothing',
                        help='Smoothing parameter. 0:polynomial smoothing, 1:first derivative, 2:second derivative, ...',
                        required=False, default=0, type=int)
    parser.add_argument('-t', '--offset',
                        help='Offset from the center point. 0:middle point, -window_size/2:last point, window_size/2 first point',
                        required=False, default=0, type=int)

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    # Get command line arguments
    args = get_arguments()

    # Compute half of window_size (rounded down)
    half_window = args.window_size // 2

    # Print resulting coefficients to terminal
    print("[", end="")
    for i, coeff in enumerate(get_coefficients(args.smoothing, args.order, args.offset, half_window)):
        end = ", " if i < args.window_size - 1 else ""
        print(f"{coeff:0.5f}", end=end)
    print("]")
