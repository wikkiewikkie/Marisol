from marisol import Marisol
from tests.mocks import MockPDF

import time
import os
import multiprocessing

if __name__ == "__main__":

    print("Creating test files...")
    file_names = []
    for num in range(1, 5001):
        bates_number = str(num).zfill(6)
        file_name = "TESTIN{}.pdf".format(bates_number)
        file_names.append(file_name)

    p = MockPDF(1)
    for file_name in file_names:
        with open(file_name, "wb") as out_file:
            out_file.write(p.read())

    print("Starting Benchmark...")
    start = time.perf_counter()

    m = Marisol("TESTOUT", 6, 1)
    for file_name in file_names:
        m.append(file_name)

    m.save()

    end = time.perf_counter()
    print("Benchmark Complete.")

    print("{} seconds elapsed.".format(end-start))
    print("{} pages per second.".format(5000/(end-start)))

    print("Cleaning up...")
    for file_name in os.listdir():
        if file_name[-4:] == ".pdf":
            os.remove(file_name)


