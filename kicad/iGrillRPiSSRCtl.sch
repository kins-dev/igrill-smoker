EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "iGrill Smoker Raspberry Pi SSR Control"
Date "2019-06-25"
Rev "**"
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
P 2750 2900
F 0 "R2" V 2543 2900 50  0000 C CNN
F 1 "R" V 2634 2900 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2680 2900 50  0001 C CNN
F 3 "~" H 2750 2900 50  0001 C CNN
	1    2750 2900
	0    1    1    0   
$EndComp
$Comp
L Device:R R1
U 1 1 5D1271D4
P 2500 3000
F 0 "R1" V 2293 3000 50  0000 C CNN
F 1 "R" V 2384 3000 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2430 3000 50  0001 C CNN
F 3 "~" H 2500 3000 50  0001 C CNN
	1    2500 3000
	0    1    1    0   
$EndComp
$Comp
L Device:LED D2
U 1 1 5D1282B8
P 2250 2900
F 0 "D2" H 2243 2645 50  0000 C CNN
F 1 "Done" H 2243 2736 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm_Clear" H 2250 2900 50  0001 C CNN
F 3 "~" H 2250 2900 50  0001 C CNN
	1    2250 2900
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D1
U 1 1 5D128CFF
P 1850 3000
F 0 "D1" H 1843 2745 50  0000 C CNN
F 1 "Low Battery" H 1843 2836 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 1850 3000 50  0001 C CNN
F 3 "~" H 1850 3000 50  0001 C CNN
	1    1850 3000
	-1   0    0    1   
$EndComp
Wire Wire Line
	3050 3000 2650 3000
Wire Wire Line
	3050 2900 2900 2900
Wire Wire Line
	2600 2900 2400 2900
Wire Wire Line
	2350 3000 2000 3000
Wire Wire Line
	2100 2900 1700 2900
Wire Wire Line
	1700 2900 1700 3000
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
P 1700 2900
F 0 "#PWR01" H 1700 2750 50  0001 C CNN
F 1 "+5V" H 1715 3073 50  0000 C CNN
F 2 "" H 1700 2900 50  0001 C CNN
F 3 "" H 1700 2900 50  0001 C CNN
	1    1700 2900
	1    0    0    -1  
$EndComp
Connection ~ 1700 2900
Wire Wire Line
	3750 2150 3750 2200
Wire Wire Line
	3650 2150 3650 2200
$Comp
L power:GND #PWR04
U 1 1 5D130239
P 4150 4950
F 0 "#PWR04" H 4150 4700 50  0001 C CNN
F 1 "GND" H 4155 4777 50  0000 C CNN
F 2 "" H 4150 4950 50  0001 C CNN
F 3 "" H 4150 4950 50  0001 C CNN
	1    4150 4950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 4950 4150 4800
Wire Wire Line
	4150 4800 4050 4800
Connection ~ 4150 4800
Connection ~ 3550 4800
Wire Wire Line
	3550 4800 3450 4800
Connection ~ 3650 4800
Wire Wire Line
	3650 4800 3550 4800
Connection ~ 3750 4800
Wire Wire Line
	3750 4800 3650 4800
Connection ~ 3850 4800
Wire Wire Line
	3850 4800 3750 4800
Connection ~ 3950 4800
Wire Wire Line
	3950 4800 3850 4800
Connection ~ 4050 4800
Wire Wire Line
	4050 4800 3950 4800
$Comp
L Device:Buzzer BZ1
U 1 1 5D130F18
P 5100 4100
F 0 "BZ1" H 5252 4129 50  0000 L CNN
F 1 "Buzzer" H 5252 4038 50  0000 L CNN
F 2 "Buzzer_Beeper:Buzzer_12x9.5RM7.6" V 5075 4200 50  0001 C CNN
F 3 "~" V 5075 4200 50  0001 C CNN
	1    5100 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 4200 4650 4200
$Comp
L power:+5V #PWR05
U 1 1 5D133C19
P 5000 3850
F 0 "#PWR05" H 5000 3700 50  0001 C CNN
F 1 "+5V" H 5100 3950 50  0000 C CNN
F 2 "" H 5000 3850 50  0001 C CNN
F 3 "" H 5000 3850 50  0001 C CNN
	1    5000 3850
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J2
U 1 1 5D13587F
P 6000 4200
F 0 "J2" H 6080 4192 50  0000 L CNN
F 1 "SSR Control" H 6080 4101 50  0000 L CNN
F 2 "Connector_Wire:SolderWirePad_1x02_P3.81mm_Drill0.8mm" H 6000 4200 50  0001 C CNN
F 3 "~" H 6000 4200 50  0001 C CNN
	1    6000 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	4650 4300 5800 4300
Wire Wire Line
	5000 3900 5000 4000
Wire Wire Line
	5000 3900 5800 3900
Wire Wire Line
	5800 3900 5800 4200
Connection ~ 5000 3900
Wire Wire Line
	5000 3850 5000 3900
$EndSCHEMATC
