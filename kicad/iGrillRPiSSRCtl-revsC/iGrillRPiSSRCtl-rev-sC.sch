EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "iGrill Smoker SSR Control Board"
Date "2019-06-26"
Rev "*C"
Comp "Redbud Farms"
Comment1 "https://creativecommons.org/licenses/by-nc-sa/4.0/"
Comment2 "License: Creative Commons BY-NC-SA"
Comment3 "https://git.kins.dev/igrill-smoker/"
Comment4 "Author: Scott Atkins (Scott@kins.dev)"
$EndDescr
$Comp
L power:+5V #PWR01
U 1 1 580C1B61
P 3100 950
F 0 "#PWR01" H 3100 800 50  0001 C CNN
F 1 "+5V" H 3100 1090 50  0000 C CNN
F 2 "" H 3100 950 50  0000 C CNN
F 3 "" H 3100 950 50  0000 C CNN
	1    3100 950 
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 950  3100 1100
Wire Wire Line
	3100 1100 2900 1100
Wire Wire Line
	3100 1200 2900 1200
Connection ~ 3100 1100
$Comp
L power:GND #PWR02
U 1 1 580C1D11
P 3000 3150
F 0 "#PWR02" H 3000 2900 50  0001 C CNN
F 1 "GND" H 3000 3000 50  0000 C CNN
F 2 "" H 3000 3150 50  0000 C CNN
F 3 "" H 3000 3150 50  0000 C CNN
	1    3000 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 1300 3000 1700
Wire Wire Line
	3000 2700 2900 2700
Wire Wire Line
	3000 2500 2900 2500
Connection ~ 3000 2700
Wire Wire Line
	3000 2000 2900 2000
Connection ~ 3000 2500
Wire Wire Line
	3000 1700 2900 1700
Connection ~ 3000 2000
$Comp
L power:GND #PWR03
U 1 1 580C1E01
P 2300 3150
F 0 "#PWR03" H 2300 2900 50  0001 C CNN
F 1 "GND" H 2300 3000 50  0000 C CNN
F 2 "" H 2300 3150 50  0000 C CNN
F 3 "" H 2300 3150 50  0000 C CNN
	1    2300 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 3000 2400 3000
Wire Wire Line
	2300 1500 2300 2300
Wire Wire Line
	2300 2300 2400 2300
Connection ~ 2300 3000
Connection ~ 2200 1100
Wire Wire Line
	2200 1900 2400 1900
Wire Wire Line
	2200 1100 2400 1100
Wire Wire Line
	2200 950  2200 1100
$Comp
L power:+3.3V #PWR04
U 1 1 580C1BC1
P 2200 950
F 0 "#PWR04" H 2200 800 50  0001 C CNN
F 1 "+3.3V" H 2200 1090 50  0000 C CNN
F 2 "" H 2200 950 50  0000 C CNN
F 3 "" H 2200 950 50  0000 C CNN
	1    2200 950 
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 1500 2400 1500
Connection ~ 2300 2300
Wire Wire Line
	2400 1200 1250 1200
Wire Wire Line
	1250 1300 2400 1300
Text Label 1250 1200 0    50   ~ 0
GPIO2(SDA1)
Text Label 1250 1300 0    50   ~ 0
GPIO3(SCL1)
Text Label 1250 1400 0    50   ~ 0
GPIO4(GCLK)
Text Label 1250 1600 0    50   ~ 0
GPIO17(GEN0)
Text Label 1250 1700 0    50   ~ 0
GPIO27(GEN2)
Text Label 1250 1800 0    50   ~ 0
GPIO22(GEN3)
Text Label 1250 2000 0    50   ~ 0
GPIO10(SPI0_MOSI)
Text Label 1250 2100 0    50   ~ 0
GPIO9(SPI0_MISO)
Text Label 1250 2200 0    50   ~ 0
GPIO11(SPI0_SCK)
Text Label 1250 2400 0    50   ~ 0
ID_SD
Text Label 1250 2500 0    50   ~ 0
GPIO5
Text Label 1250 2600 0    50   ~ 0
GPIO6
Text Label 1250 2700 0    50   ~ 0
GPIO13(PWM1)
Text Label 1250 2800 0    50   ~ 0
GPIO19(SPI1_MISO)
Text Label 1250 2900 0    50   ~ 0
GPIO26
Text Label 3950 2900 2    50   ~ 0
GPIO20(SPI1_MOSI)
Text Label 3950 2800 2    50   ~ 0
GPIO16
Text Label 3950 2600 2    50   ~ 0
GPIO12(PWM0)
Text Label 3950 2400 2    50   ~ 0
ID_SC
Text Label 3950 2300 2    50   ~ 0
GPIO7(SPI1_CE_N)
Text Label 3950 2200 2    50   ~ 0
GPIO8(SPI0_CE_N)
Text Label 3950 2100 2    50   ~ 0
GPIO25(GEN6)
Text Label 3950 1900 2    50   ~ 0
GPIO24(GEN5)
Text Label 3950 1800 2    50   ~ 0
GPIO23(GEN4)
Text Label 3950 1600 2    50   ~ 0
GPIO18(GEN1)(PWM0)
Text Label 3950 1500 2    50   ~ 0
GPIO15(RXD0)
Text Label 3950 1400 2    50   ~ 0
GPIO14(TXD0)
Wire Wire Line
	3000 1300 2900 1300
Connection ~ 3000 1700
Text Notes 650  7600 0    50   ~ 0
ID_SD and ID_SC PINS:\nThese pins are reserved for HAT ID EEPROM.\n\nAt boot time this I2C interface will be\ninterrogated to look for an EEPROM\nthat identifes the attached board and\nallows automagic setup of the GPIOs\n(and optionally, Linux drivers).\n\nDO NOT USE these pins for anything other\nthan attaching an I2C ID EEPROM. Leave\nunconnected if ID EEPROM not required.
$Comp
L iGrillRPiSSRCtl-rev-sC-rescue:Mounting_Hole-Mechanical MK1
U 1 1 5834FB2E
P 3000 7200
F 0 "MK1" H 3100 7246 50  0000 L CNN
F 1 "M2.5" H 3100 7155 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5" H 3000 7200 60  0001 C CNN
F 3 "" H 3000 7200 60  0001 C CNN
	1    3000 7200
	1    0    0    -1  
$EndComp
$Comp
L iGrillRPiSSRCtl-rev-sC-rescue:Mounting_Hole-Mechanical MK3
U 1 1 5834FBEF
P 3450 7200
F 0 "MK3" H 3550 7246 50  0000 L CNN
F 1 "M2.5" H 3550 7155 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5" H 3450 7200 60  0001 C CNN
F 3 "" H 3450 7200 60  0001 C CNN
	1    3450 7200
	1    0    0    -1  
$EndComp
$Comp
L iGrillRPiSSRCtl-rev-sC-rescue:Mounting_Hole-Mechanical MK2
U 1 1 5834FC19
P 3000 7400
F 0 "MK2" H 3100 7446 50  0000 L CNN
F 1 "M2.5" H 3100 7355 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5" H 3000 7400 60  0001 C CNN
F 3 "" H 3000 7400 60  0001 C CNN
	1    3000 7400
	1    0    0    -1  
$EndComp
$Comp
L iGrillRPiSSRCtl-rev-sC-rescue:Mounting_Hole-Mechanical MK4
U 1 1 5834FC4F
P 3450 7400
F 0 "MK4" H 3550 7446 50  0000 L CNN
F 1 "M2.5" H 3550 7355 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_M2.5" H 3450 7400 60  0001 C CNN
F 3 "" H 3450 7400 60  0001 C CNN
	1    3450 7400
	1    0    0    -1  
$EndComp
Text Notes 3000 7050 0    50   ~ 0
Mounting Holes
$Comp
L Connector_Generic:Conn_02x20_Odd_Even P1
U 1 1 59AD464A
P 2600 2000
F 0 "P1" H 2650 3117 50  0000 C CNN
F 1 "Conn_02x20_Odd_Even" H 2650 3026 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical" H -2250 1050 50  0001 C CNN
F 3 "" H -2250 1050 50  0001 C CNN
	1    2600 2000
	1    0    0    -1  
$EndComp
Text Label 3950 3000 2    50   ~ 0
GPIO21(SPI1_SCK)
Wire Wire Line
	3100 1100 3100 1150
Wire Wire Line
	3000 2700 3000 3150
Wire Wire Line
	3000 2500 3000 2700
Wire Wire Line
	3000 2000 3000 2500
Wire Wire Line
	2300 3000 2300 3150
Wire Wire Line
	2200 1100 2200 1900
Wire Wire Line
	2300 2300 2300 3000
Wire Wire Line
	3000 1700 3000 2000
NoConn ~ 4050 2400
NoConn ~ 1150 2400
Wire Wire Line
	2900 2400 4050 2400
Wire Wire Line
	1150 2400 2400 2400
Wire Wire Line
	4150 2800 4150 2900
Wire Wire Line
	2900 2900 4150 2900
Wire Wire Line
	4150 2900 4150 3000
Wire Wire Line
	2900 3000 4150 3000
Connection ~ 4150 2900
Wire Wire Line
	4150 2100 4150 2200
Wire Wire Line
	2900 2300 4150 2300
Wire Wire Line
	2900 2100 4150 2100
Wire Wire Line
	2900 2200 4150 2200
Connection ~ 4150 2200
Wire Wire Line
	4150 2200 4150 2300
$Comp
L power:+5V #PWR0101
U 1 1 5D1449BC
P 4150 2800
F 0 "#PWR0101" H 4150 2650 50  0001 C CNN
F 1 "+5V" H 4150 2940 50  0000 C CNN
F 2 "" H 4150 2800 50  0000 C CNN
F 3 "" H 4150 2800 50  0000 C CNN
	1    4150 2800
	1    0    0    -1  
$EndComp
Connection ~ 4150 2800
Wire Wire Line
	2900 2800 4150 2800
$Comp
L power:GND #PWR0102
U 1 1 5D145865
P 4150 2300
F 0 "#PWR0102" H 4150 2050 50  0001 C CNN
F 1 "GND" H 4150 2150 50  0000 C CNN
F 2 "" H 4150 2300 50  0000 C CNN
F 3 "" H 4150 2300 50  0000 C CNN
	1    4150 2300
	1    0    0    -1  
$EndComp
Connection ~ 4150 2300
Wire Wire Line
	2900 1900 4150 1900
Wire Wire Line
	2900 1400 4150 1400
Wire Wire Line
	2900 1800 4150 1800
Connection ~ 4150 1800
Wire Wire Line
	4150 1800 4150 1900
Wire Wire Line
	2900 1600 4150 1600
Wire Wire Line
	4150 1600 4150 1800
Wire Wire Line
	4150 1900 4150 2100
Connection ~ 4150 1900
Connection ~ 4150 2100
Connection ~ 3100 1150
Wire Wire Line
	3100 1150 3100 1200
$Comp
L Device:R R1
U 1 1 5D14E11D
P 1100 1200
F 0 "R1" V 1000 1200 50  0000 C CNN
F 1 "100" V 1100 1200 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 1030 1200 50  0001 C CNN
F 3 "~" H 1100 1200 50  0001 C CNN
	1    1100 1200
	0    1    1    0   
$EndComp
$Comp
L Device:R R2
U 1 1 5D14F1BC
P 1100 1300
F 0 "R2" V 1200 1300 50  0000 C CNN
F 1 "100" V 1100 1300 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 1030 1300 50  0001 C CNN
F 3 "~" H 1100 1300 50  0001 C CNN
	1    1100 1300
	0    1    1    0   
$EndComp
$Comp
L Device:LED_ALT D1
U 1 1 5D14FA39
P 750 1050
F 0 "D1" H 743 795 50  0000 C CNN
F 1 "Low Battery" H 743 886 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 750 1050 50  0001 C CNN
F 3 "~" H 750 1050 50  0001 C CNN
	1    750  1050
	-1   0    0    1   
$EndComp
$Comp
L Device:LED_ALT D2
U 1 1 5D150925
P 750 1450
F 0 "D2" H 743 1195 50  0000 C CNN
F 1 "Done" H 743 1286 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm_Clear" H 750 1450 50  0001 C CNN
F 3 "~" H 750 1450 50  0001 C CNN
	1    750  1450
	-1   0    0    1   
$EndComp
Wire Wire Line
	600  1050 600  1250
Wire Wire Line
	950  1300 950  1450
Wire Wire Line
	950  1450 900  1450
Wire Wire Line
	900  1050 950  1050
Wire Wire Line
	950  1050 950  1200
$Comp
L power:+5V #PWR0103
U 1 1 5D15862C
P 550 850
F 0 "#PWR0103" H 550 700 50  0001 C CNN
F 1 "+5V" H 550 990 50  0000 C CNN
F 2 "" H 550 850 50  0000 C CNN
F 3 "" H 550 850 50  0000 C CNN
	1    550  850 
	1    0    0    -1  
$EndComp
Wire Wire Line
	550  850  550  1250
Wire Wire Line
	550  1250 600  1250
Connection ~ 600  1250
Wire Wire Line
	600  1250 600  1450
$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 5D15A837
P 650 2900
F 0 "J1" V 522 2712 50  0000 R CNN
F 1 "Conn_01x02" V 800 2950 50  0000 R CNN
F 2 "Connector_Wire:SolderWirePad_1x02_P3.81mm_Drill0.8mm" H 650 2900 50  0001 C CNN
F 3 "~" H 650 2900 50  0001 C CNN
	1    650  2900
	0    -1   1    0   
$EndComp
Wire Wire Line
	750  2700 2400 2700
Wire Wire Line
	550  1250 550  2700
Wire Wire Line
	550  2700 650  2700
Connection ~ 550  1250
Connection ~ 4150 3000
$Comp
L Device:Buzzer BZ1
U 1 1 5D165E77
P 4950 2800
F 0 "BZ1" V 4908 2952 50  0000 L CNN
F 1 "Buzzer" V 4999 2952 50  0000 L CNN
F 2 "Buzzer_Beeper:Buzzer_TDK_PS1240P02BT_D12.2mm_H6.5mm" V 4925 2900 50  0001 C CNN
F 3 "~" V 4925 2900 50  0001 C CNN
	1    4950 2800
	0    1    1    0   
$EndComp
Wire Wire Line
	2900 2600 4300 2600
NoConn ~ 1150 1600
NoConn ~ 1150 1700
NoConn ~ 1150 1800
NoConn ~ 1150 2500
NoConn ~ 1150 2600
NoConn ~ 1150 2800
NoConn ~ 1150 2900
NoConn ~ 1200 1450
Wire Wire Line
	1200 1450 1200 1400
Wire Wire Line
	1200 1400 2400 1400
Wire Wire Line
	1150 1600 2400 1600
Wire Wire Line
	1150 1700 2400 1700
Wire Wire Line
	1150 1800 2400 1800
Wire Wire Line
	1150 2500 2400 2500
Wire Wire Line
	1150 2600 2400 2600
Wire Wire Line
	1150 2800 2400 2800
Wire Wire Line
	1150 2900 2400 2900
NoConn ~ 1150 2000
NoConn ~ 1150 2100
NoConn ~ 1150 2200
Wire Wire Line
	1150 2000 2400 2000
Wire Wire Line
	1150 2100 2400 2100
Wire Wire Line
	1150 2200 2400 2200
Wire Wire Line
	4150 3000 5550 3000
$Comp
L Switch:SW_DPDT_x2 SW1
U 1 1 5D19CE23
P 4500 2600
F 0 "SW1" H 4500 2885 50  0000 C CNN
F 1 "SW_DPDT_x2" H 4500 2794 50  0000 C CNN
F 2 "Button_Switch_THT:SW_CuK_JS202011CQN_DPDT_Straight" H 4500 2600 50  0001 C CNN
F 3 "~" H 4500 2600 50  0001 C CNN
	1    4500 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 2700 4850 2700
Wire Wire Line
	5050 2700 5550 2700
Wire Wire Line
	5550 2700 5550 3000
Wire Wire Line
	4700 2500 5550 2500
NoConn ~ 5550 2500
Wire Wire Line
	4500 1500 4500 1150
Wire Wire Line
	2900 1500 4500 1500
Wire Wire Line
	3100 1150 4500 1150
Wire Wire Line
	4150 1400 4150 1600
Connection ~ 4150 1600
$EndSCHEMATC
