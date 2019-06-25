EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "iGrill Smoker Raspberry Pi SSR Control"
Date "2019-06-25"
Rev "*A"
Comp "Redbud Farms"
Comment1 "https://git.kins.dev/igrill-smoker/"
Comment2 "https://creativecommons.org/licenses/by-nc-sa/4.0/"
Comment3 "License: Creative Commons BY-NC-SA"
Comment4 "Author: Scott Atkins (Scott@kins.dev)"
$EndDescr
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 5D121ED7
P 3850 3500
F 0 "J1" H 3450 4800 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 4450 4800 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical" H 3850 3500 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 3850 3500 50  0001 C CNN
	1    3850 3500
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5D125B97
P 2750 3700
F 0 "R2" V 2650 3700 50  0000 C CNN
F 1 "R" V 2750 3700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2680 3700 50  0001 C CNN
F 3 "~" H 2750 3700 50  0001 C CNN
	1    2750 3700
	0    1    1    0   
$EndComp
$Comp
L Device:R R1
U 1 1 5D1271D4
P 2500 3800
F 0 "R1" V 2600 3800 50  0000 C CNN
F 1 "R" V 2500 3800 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2430 3800 50  0001 C CNN
F 3 "~" H 2500 3800 50  0001 C CNN
	1    2500 3800
	0    1    1    0   
$EndComp
$Comp
L Device:LED D2
U 1 1 5D1282B8
P 2250 3700
F 0 "D2" H 2400 3600 50  0000 C CNN
F 1 "Done" H 2243 3536 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm_Clear" H 2250 3700 50  0001 C CNN
F 3 "~" H 2250 3700 50  0001 C CNN
	1    2250 3700
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D1
U 1 1 5D128CFF
P 1850 3800
F 0 "D1" H 2100 3800 50  0000 C CNN
F 1 "Low Battery" H 1850 3900 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 1850 3800 50  0001 C CNN
F 3 "~" H 1850 3800 50  0001 C CNN
	1    1850 3800
	-1   0    0    1   
$EndComp
Wire Wire Line
	3050 3800 2650 3800
Wire Wire Line
	3050 3700 2900 3700
Wire Wire Line
	2600 3700 2400 3700
Wire Wire Line
	2350 3800 2000 3800
Wire Wire Line
	2100 3700 1700 3700
Wire Wire Line
	1700 3700 1700 3800
$Comp
L power:+5V #PWR02
U 1 1 5D12D9CE
P 3650 2150
F 0 "#PWR02" H 3650 2000 50  0001 C CNN
F 1 "+5V" H 3550 2250 50  0000 C CNN
F 2 "" H 3650 2150 50  0001 C CNN
F 3 "" H 3650 2150 50  0001 C CNN
	1    3650 2150
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR03
U 1 1 5D12E0C5
P 3750 2150
F 0 "#PWR03" H 3750 2000 50  0001 C CNN
F 1 "+5V" H 3850 2250 50  0000 C CNN
F 2 "" H 3750 2150 50  0001 C CNN
F 3 "" H 3750 2150 50  0001 C CNN
	1    3750 2150
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR01
U 1 1 5D12E56D
P 1700 3700
F 0 "#PWR01" H 1700 3550 50  0001 C CNN
F 1 "+5V" H 1715 3873 50  0000 C CNN
F 2 "" H 1700 3700 50  0001 C CNN
F 3 "" H 1700 3700 50  0001 C CNN
	1    1700 3700
	1    0    0    -1  
$EndComp
Connection ~ 1700 3700
Wire Wire Line
	3750 2150 3750 2200
Wire Wire Line
	3650 2150 3650 2200
$Comp
L Device:Buzzer BZ1
U 1 1 5D130F18
P 5050 4400
F 0 "BZ1" H 5202 4429 50  0000 L CNN
F 1 "Buzzer" H 5202 4338 50  0000 L CNN
F 2 "Buzzer_Beeper:Buzzer_12x9.5RM7.6" V 5025 4500 50  0001 C CNN
F 3 "~" V 5025 4500 50  0001 C CNN
	1    5050 4400
	0    1    1    0   
$EndComp
$Comp
L power:+5V #PWR05
U 1 1 5D133C19
P 5350 3850
F 0 "#PWR05" H 5350 3700 50  0001 C CNN
F 1 "+5V" H 5450 3950 50  0000 C CNN
F 2 "" H 5350 3850 50  0001 C CNN
F 3 "" H 5350 3850 50  0001 C CNN
	1    5350 3850
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J2
U 1 1 5D13587F
P 5650 4300
F 0 "J2" H 5730 4292 50  0000 L CNN
F 1 "SSR Control" H 5730 4201 50  0000 L CNN
F 2 "Connector_Wire:SolderWirePad_1x02_P3.81mm_Drill0.8mm" H 5650 4300 50  0001 C CNN
F 3 "~" H 5650 4300 50  0001 C CNN
	1    5650 4300
	1    0    0    1   
$EndComp
Wire Wire Line
	5450 4200 4650 4200
Wire Wire Line
	4650 4300 4950 4300
Wire Wire Line
	5150 4300 5350 4300
Wire Wire Line
	5350 4300 5350 3850
Connection ~ 5350 4300
Wire Wire Line
	5350 4300 5450 4300
$EndSCHEMATC
