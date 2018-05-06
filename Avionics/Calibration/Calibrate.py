import time, pigpio, os
import MPU9250

class Calibrate(object):

  def __init__(self):
      # Most sensors share a pigpio object to control enable pins
      self.piggy = pigpio.pi()

      # Use the GPIO number, NOT the pin number!
      self.mpuA = MPU9250.MPU9250(pi=self.piggy, gpio=17)
      self.mpuB = MPU9250.MPU9250(pi=self.piggy, gpio=27)
      self.mpuC = MPU9250.MPU9250(pi=self.piggy, gpio=22)


  def runLoop(self, num=True):
    tot_x_17 = 0
    tot_x_27 = 0
    tot_x_22 = 0
    tot_y_17 = 0
    tot_y_27 = 0
    tot_y_22 = 0
    tot_z_17 = 0
    tot_z_27 = 0
    tot_z_22 = 0

    mean_x_17 = 0
    mean_x_27 = 0
    mean_x_22 = 0
    mean_y_17 = 0
    mean_y_27 = 0
    mean_y_22 = 0
    mean_z_17 = 0
    mean_z_27 = 0
    mean_z_22 = 0

    totc_x_17 = 0
    totc_x_27 = 0
    totc_x_22 = 0
    totc_y_17 = 0
    totc_y_27 = 0
    totc_y_22 = 0
    totc_z_17 = 0
    totc_z_27 = 0
    totc_z_22 = 0

    meanc_x_17 = 0
    meanc_x_27 = 0
    meanc_x_22 = 0
    meanc_y_17 = 0
    meanc_y_27 = 0
    meanc_y_22 = 0
    meanc_z_17 = 0
    meanc_z_27 = 0
    meanc_z_22 = 0

    loops = 0
    while(num):
        if num is not True: num -= 1

        loops += 1
        data = {}
        for x,y in [('17_',self.mpuA), ('27_', self.mpuB), ('22_', self.mpuC)]:
            data.update( {x+k:v for k,v in y.read_all().items()} )

        tot_x_17 += data['17_acc_x']
        tot_x_27 += data['27_acc_x']
        tot_x_22 += data['22_acc_x']
        tot_y_17 += data['17_acc_y']
        tot_y_27 += data['27_acc_y']
        tot_y_22 += data['22_acc_y']
        tot_z_17 += data['17_acc_z']
        tot_z_27 += data['27_acc_z']
        tot_z_22 += data['22_acc_z']

        mean_x_17 = tot_x_17/loops
        mean_x_27 = tot_x_27/loops
        mean_x_22 = tot_x_22/loops
        mean_y_17 = tot_y_17/loops
        mean_y_27 = tot_y_27/loops
        mean_y_22 = tot_y_22/loops
        mean_z_17 = tot_z_17/loops
        mean_z_27 = tot_z_27/loops
        mean_z_22 = tot_z_22/loops

        totc_x_17 += data['17_gyro_x']
        totc_x_27 += data['27_gyro_x']
        totc_x_22 += data['22_gyro_x']
        totc_y_17 += data['17_gyro_y']
        totc_y_27 += data['27_gyro_y']
        totc_y_22 += data['22_gyro_y']
        totc_z_17 += data['17_gyro_z']
        totc_z_27 += data['27_gyro_z']
        totc_z_22 += data['22_gyro_z']

        meanc_x_17 = totc_x_17/loops
        meanc_x_27 = totc_x_27/loops
        meanc_x_22 = totc_x_22/loops
        meanc_y_17 = totc_y_17/loops
        meanc_y_27 = totc_y_27/loops
        meanc_y_22 = totc_y_22/loops
        meanc_z_17 = totc_z_17/loops
        meanc_z_27 = totc_z_27/loops
        meanc_z_22 = totc_z_22/loops

    print(meanc_x_17, meanc_x_27, meanc_x_22, meanc_y_17, meanc_y_27, meanc_y_22, meanc_z_17, meanc_z_27, meanc_z_22)
    print(mean_x_17, mean_x_27, mean_x_22, mean_y_17, mean_y_27, mean_y_22, mean_z_17, mean_z_27, mean_z_22)
    acc_17_offsets = self.mpuA.calibrate_accel(mean_x_17,mean_y_17,mean_z_17)
    acc_27_offsets = self.mpuB.calibrate_accel(mean_x_27,mean_y_27,mean_z_27)
    acc_22_offsets = self.mpuC.calibrate_accel(mean_x_22,mean_y_22,mean_z_22)
    gyro_17_offsets = self.mpuA.calibrate_gyro(meanc_x_17,meanc_y_17,meanc_z_17)
    gyro_27_offsets = self.mpuB.calibrate_gyro(meanc_x_27,meanc_y_27,meanc_z_27)
    gyro_22_offsets = self.mpuC.calibrate_gyro(meanc_x_22,meanc_y_22,meanc_z_22)

    with open("calibration_values.csv", "w") as csv_out:
        csv_out.write(
            "accel_17 = [{:>5},{:>5},{:>5}]\n" \
            "accel_27 = [{:>5},{:>5},{:>5}]\n" \
            "accel_22 = [{:>5},{:>5},{:>5}]\n" \
            "gyro_17  = [{:>5},{:>5},{:>5}]\n"  \
            "gyro_27  = [{:>5},{:>5},{:>5}]\n"  \
            "gyro_22  = [{:>5},{:>5},{:>5}]\n".format(
                *acc_17_offsets,
                *acc_27_offsets,
                *acc_22_offsets,
                *gyro_17_offsets,
                *gyro_27_offsets,
                *gyro_22_offsets
            )
        )
    print("Created 'calibration_values.csv' file with calibration values.")

if __name__ == "__main__":
    calibrate = Calibrate()
    calibrate.runLoop(10)
    calibrate.runLoop(10)
