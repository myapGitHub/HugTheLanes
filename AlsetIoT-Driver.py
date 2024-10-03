

class Driver:
    def __init__(self):
        self.inSeat = False
        self.handsOnWheel = False
        self.isAwake = False

    def __str__(self) -> str:
        return "Driver is in seat " if self.inSeat else "Driver is not in seat "

class Sensors: 
    def __init__(self, Driver):
        self.Driver = Driver
        self.leftDistanceSensor, self.rightDistanceSensor, self.frontDistanceSensor, self.rearDistanceSensor = 0.00, 0.00, 0.00, 0.00
        self.leftDistanceCamera, self.rightDistanceCamera, self.frontDistanceCamera, self.rearDistanceCamera = 0.00, 0.00, 0.00, 0.00
        self.tirePressure = [0.00, 0.00, 0.00, 0.00]
        self.steeringWheelSensor = False
        self.driverAwakeCamera = False
        self.gasInTank = 0.00
        self.lightLevels = 0.00
        self.adaptiveCruiseControlSwitch = False
        self.weatherAndRoadAdaptationSwitch = False
        self.blinker = [False, False]

    def handsOnWheel(self) -> bool:
        return self.steeringWheelSensor

    def driverAlert(self) -> None:
        return self.isAwake

    def getBlinker(self) -> list:
        return self.blinker

    #changed this to list so it returns a list of all 4 directions rather than making multiple individual calls
    def getDistance(self) -> list:
        return [self.leftDistanceSensor, self.rightDistanceSensor, self.frontDistanceSensor, self.rearDistanceSensor]

    def getGasInTank(self) -> float:
        return self.gasInTank

    def getTirePressure(self) -> list:
        return self.tirePressure

    def getHeadlightLevel(self) -> float:
        return self.lightLevels

    def getAdaptiveCruiseControl(self) -> bool:
        return self.adaptiveCruiseControlSwitch
    
    def getWeatherAndRoadAdaptation(self) -> bool:
        return self.weatherAndRoadAdaptationSwitch

    def getAwakeStatus(self) -> bool:
        return (self.driverAwakeCamera and self.steeringWheelSensor)

    def getInSeat(self) -> bool:
        return self.inSeat
    
        
class VCS: 
    def __init__(self, Sensors):
        self.Sensors = Sensors
        self.isOn = False
        self.inSeat = False
        self.inMotion = False
        self.vehicleSpeed = 0
        self.obstacleDistance = 0
        self.accelerationLevel = 0
        self.brakeLevel = 0
        self.trafficLightColor = ""
        self.leavingLane = False
        self.steerAngle = 0
        self.selfVehicleSpeed = 0
        self.otherVehicleSpeed = 0
        self.weatherCondition = ""
        self.windSheildLevel = 0 
        self.direction = ""

    def __str__(self):
        return "Car is on." if self.isOn else "Car is not on."

    #sensor that alerts the driver of vehicle in blindspot
    def blindSpotMonitor(self) -> bool:
        return self.vehicleInBlindSpot()

    #ues left and right distance sensors to sense if a car is ot the right or left and less the 5 feet away being in their blindspot 
    def vehicleInBlindSpot(self) -> bool:
        if self.Sensors.leftDistance < 5 or self.Sensors.rightDistance < 5:
            return True
        else:
            return False

    def parkingAssist(self) -> None: 
        obstacle1 = self.Sensors.frontDistanceCamera 
        obstacle2 = self.Sensors.rearDistanceCamera
        space = obstacle1-obstacle2

        if self.openParkingSpot:
            if space == 9:
                if self.Sensors.leftDistanceCamera > 10:
                    self.steerAngle = -90
                else:
                    self.steerAngle = 90
            else:
                if self.Sensors.leftDistanceCamera > 20:
                    self.steerAngle = -25
                    self.direction = "Reverse"
                    if self.Sensors.rearDistanceCamera < 3:
                        self.steerAngle = 45
                else:
                    self.steerAngle = 25
                    self.direction = "Reverse"
                    if self.Sensors.rearDistanceCamera < 3:
                        self.steerAngle = -45


    #uses right and left distance cameras to determin the distance from the lane lines greater then two implies proper and safe distance
    def withinLines(self) -> bool:
        if self.inMotion == True:
            if self.Sensors.rightDistanceCamera > 2 and self.Sensors.leftDistanceCamera > 2:
                return True
        else:
            return False

    #using front and rear cameras to get distances or two vehicles and determining if there is a safe distance in between open to park
    #9 feet for regular parking 20 feet for parallel
    def openParkingSpot(self) -> bool:
        obstacle1 = self.Sensors.frontDistanceCamera 
        obstacle2 = self.Sensors.rearDistanceCamera
        space = obstacle1-obstacle2
        if  space == 9:
            return True
        elif space == 20:
            return True
        else:
            return False

    #changed this to list so it returns a list of all 4 directions rather than making multiple individual calls
    def getObstacleDistance(self) -> list:
        return [self.Sensors.frontDistanceCamera, self.Sensors.rearDistanceCamera, self.Sensors.leftDistanceCamera, self.Sensors.rightDistanceCamera]

    #uses result of withinlines to determine if lane departure is happening
    def laneDeparture(self) -> bool:
        if self.withinLines() == False:
            self.leavingLane = True
            return True

    #if leaving lane is true
    def isLeavingLane(self) -> bool:
        if self.leavingLane == True:
            return True
        else:
            return False

    #sound and warning is only emmited if there is no blinker on
    #blinker on implies intent to change lanes
    def emitLeaveLaneSound(self) -> bool:
        if self.Sensors.blinker[0] == True or self.Sensors.blinker[1] == True:
            return False
        elif self.leavingLane == True:
            return True
        else:
            return False

    #if the car is approaching an obstacle under 50 ft applie different brake levels depending on the distance of obstacle, and speed of vehicle
    #exeption if the left or right lanes are open and the car can swerve to the side
    def collisionAvoidance(self) -> None:
        if self.inMotion == True:
            if self.Sensors.frontDistanceSensor < 50:
                if self.Sensors.frontDistanceSensor > 35:
                    if self.vehicleSpeed > 50:
                        if self.Sensors.leftDistanceCamera > 50:
                            self.steerAngle = -25
                        elif self.Sensors.rightDistanceCamera > 50:
                            self.steerAngle = 25
                        else: 
                            self.brakeLevel = 2
                    
                    if self.vehicleSpeed < 50:
                        if self.Sensors.leftDistanceCamera > 50:
                            self.steerAngle = -25
                        elif self.Sensors.rightDistanceCamera > 50:
                            self.steerAngle = 25
                        else: 
                            self.brakeLevel = 1
                if self.Sensors.frontDistanceSensor > 25:
                    if self.vehicleSpeed > 50:
                        if self.Sensors.leftDistanceCamera > 50:
                            self.steerAngle = -25
                        elif self.Sensors.rightDistanceCamera > 50:
                            self.steerAngle = 25
                        else: 
                            self.brakeLevel = 3
                    
                    if self.vehicleSpeed < 50:
                        if self.Sensors.leftDistanceCamera > 50:
                            self.steerAngle = -25
                        elif self.Sensors.rightDistanceCamera > 50:
                            self.steerAngle = 25
                        else: 
                            self.brakeLevel = 2
                if self.Sensors.frontDistanceSensor <= 25:
                    if self.vehicleSpeed > 50:
                        if self.Sensors.leftDistanceCamera > 50:
                            self.steerAngle = -25
                        elif self.Sensors.rightDistanceCamera > 50:
                            self.steerAngle = 25
                        else: 
                            self.brakeLevel = 3
                    
                    if self.vehicleSpeed < 50:
                        if self.Sensors.leftDistanceCamera > 50:
                            self.steerAngle = -25
                        elif self.Sensors.rightDistanceCamera > 50:
                            self.steerAngle = 25
                        else: 
                            self.brakeLevel = 3

    #changed this to degree instead of having a separate function for left and right, can use - as left and + as right
    def intSteer(degree, self) -> int:
        self.steerAngle = degree

    def setAccelerationLevel(self, level) -> None:
        if level < 0: 
            print("Value cannot be less than 0")
        else: 
            self.accelerationLevel = level

    def getAccelerationLevel(self) -> int:
        return self.accelerationLevel

    def setBrakeLevel(self, level) -> None:
        if level < 0: 
            print("Value cannot be less than 0")
        else: 
            self.brakeLevel = level

    def getBrakeLevel(self) -> int:
        return self.brakeLevel

    def autoBrake(self) -> None: #Set appropriate brake level depending on obstacle distance
        if self.Sensors.ObstacleDistance(self) > 26:
            self.brakeLevel = 1
        elif self.Sensors.getDistance(self) > 15:
            self.brakeLevel = 2
        else:
            self.brakeLevel = 3

    def autoBrakeStatus(self) -> bool: #Return true if auto brake is on, false otherwise
        if self.brakeLevel > 0:
            return True
        else:
            return False

    def adaptiveCruiseControl(self) -> None: #Sets adaptiveCruiseControl to true if called
        self.Sensors.adaptiveCruiseControlSwitch = True

    def adaptiveCruiseControlStatus(self) -> bool:
        return self.Sensors.getAdaptiveCruiseControl()

    def getOtherVehicleSpeed(self) -> int: #Returns vechile speed of another car
        return self.otherVehicleSpeed

    def getSelfVehicleSpeed(self) -> int:
        return self.vehicleSpeed

    def weatherAndRoadAdaptation(self, weather): #Sets weatherCondition to true if called
        valid_conditions = ["rain", "snow"]
        if weather in valid_conditions:
            self.weatherCondition = weather
            self.Sensors.weatherAndRoadAdaptationSwitch = True
        else:
            self.weatherCondition = "clear"
            self.Sensors.weatherAndRoadAdaptationSwitch = False 

    def weatherAndRoadAdaptationStatus(self) -> bool: #Returns current weather condition, true if bad weather, false otherwise
        return self.Sensors.getWeatherAndRoadAdaptation()

    def setWindshieldLevel(self, level) -> None: #Sets windshild wiper level to specified level
        if self.Sensors.getWeatherAndRoadAdaptation()== True:
            self.windShieldLevel = level
        else:
            print("Current weather does not fulfill windshield conditions")

    def getWindshieldLevel(self) -> int: #Returns windshield level
        return self.windShieldLevel

    def getWeather(self) -> str:  #Returns weather condition
        return self.weatherCondition

    #if there are no blinkers assume going straight and reads the traffic light color to determine action
    #same for if blinker is on except it turns the steering wheel
    def intersectionAssist(self) -> None:
        if self.inMotion:
            if self.Sensors.blinker[0] == False and self.Sensors.blinker[1] == False:
                if self.trafficLightColor == "Yellow":
                    if self.Sensors.frontDistanceSensor > 10:
                        self.brakeLevel = 1
                elif self.trafficLightColor == "Red":
                    self.brakeLevel = 1
            elif self.Sensors.blinker[0] == True:
                if self.trafficLightColor == "Green":
                    self.steeringAngle = -90
                elif self.trafficLightColor == "Yellow":
                    if self.Sensors.frontDistanceSensor > 10:
                        self.brakeLevel = 1
                    else:
                        self.steeringAngle = -90
                else:
                    self.brakeLevel = 1
            else:
                if self.trafficLightColor == "Green":
                    self.steeringAngle = 90
                elif self.trafficLightColor == "Yellow":
                    if self.Sensors.frontDistanceSensor > 10:
                        self.brakeLevel = 1
                    else:
                        self.steeringAngle = 90
                else:
                    self.brakeLevel = 1

    def getTrafficLight(self) -> str: #Returns traffic light color 
        return self.trafficLightColor

    #flat tire occurrs if it is low pressure alert driver if it is dengerously flat alert driver and safley pull over
    #maintence check on gas levels as well
    def maintenanceMonitor(self) -> None:
        if self.Sensors.tirePressure[0] < 30 or self.Sensors.tirePressure[1] < 30 or self.Sensors.tirePressure[2] < 30 or self.Sensors.tirePressure[3] < 30:
            if self.Sensors.tirePressure[0] > 20 or self.Sensors.tirePressure[1] > 20 or self.Sensors.tirePressure[2] > 20 or self.Sensors.tirePressure[3] > 20:
                print("TIRE PRESSURE LOW")
            else:
                print("FLAT TIRE, PULL OVER")
                if self.Sensors.rightDistanceSensor > 50:
                    self.steerAngle = 20
                    self.brakeLevel = 1
                    self.inMotion = False

        if self.Sensors.gasInTank < 20:
            print("LOW ON GAS")
                    
    def driverMonitor(self) -> None:
        if self.driverMonitorStatus() == False:
            print("ALERT DRIVER")

    def driverMonitorStatus(self) -> bool:
        return self.Sensors.getAwakeStatus()

class Car:
    def __init__(self, VCS):
        self.VCS = VCS

    def __str__(self) -> str:
        return self.VCS.Sensors.Driver.__str__() + "and " + self.VCS.__str__()


Driver1 = Driver()
Sensors1 = Sensors(Driver1)
VCS1 = VCS(Sensors1)
car1 = Car(VCS1)
print(car1.VCS.driverMonitor())
car1.VCS.setBrakeLevel(-3)
print(car1.VCS.adaptiveCruiseControlStatus())

print(car1.__str__())