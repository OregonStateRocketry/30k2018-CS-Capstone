from MPU6050 import MPU6050
# import pigpio

# pi = pigpio.pi()

# These are using GPIO.BOARD, use the PIN number, NOT the GPIO number!
mpuA = MPU6050(0x69, 11)
mpuB = MPU6050(0x69, 13)
mpuC = MPU6050(0x69, 15)

with open('raw_demoBlockReads_data.txt', 'w') as f:
    # Write a header line
    f.write("Payload_Avionics\n")
    f.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
        'm1.roll(rad)', 'm1.pitch(rad)', 'm1.ax', 'm1.ay', 'm1.az',
        'm2.roll(rad)', 'm2.pitch(rad)', 'm2.ax', 'm2.ay', 'm2.az',
        'm3.roll(rad)', 'm3.pitch(rad)', 'm3.ax', 'm3.ay', 'm3.az'
    ))

    for i in range(1000):
        m1 = mpuA.read_most()
        m2 = mpuB.read_most()
        m3 = mpuC.read_most()
        # print("{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},\t{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\n".format(
        #     m1['roll'], m1['pitch'], m1['acc_x'], m1['acc_y'], m1['acc_z'],
        #     m2['roll'], m2['pitch'], m2['acc_x'], m2['acc_y'], m2['acc_z'],
        #     m3['roll'], m3['pitch'], m3['acc_x'], m3['acc_y'], m3['acc_z']
        # ))
        f.write("{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"\
                "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"\
                "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\n".format(
            m1['roll'], m1['pitch'], m1['acc_x'], m1['acc_y'], m1['acc_z'],
            m2['roll'], m2['pitch'], m2['acc_x'], m2['acc_y'], m2['acc_z'],
            m3['roll'], m3['pitch'], m3['acc_x'], m3['acc_y'], m3['acc_z']
        ))

print("Done!")
