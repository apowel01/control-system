# Dictionary for CAN-Bus

# Define relation between CAN id and message name
ids =  {
	280 : 'Motor 1 Recieved',
	281 : 'Motor 1 data',
	296 : 'Motor 2 Recieved',
	297 : 'Motor 2 data',
	312 : 'Motor 3 Recieved',
	313 : 'Motor 3 data',
	328 : 'Motor 4 Recieved',
	329 : 'Motor 4 data',
	344 : 'Motor 5 Recieved',
	345 : 'Motor 5 data',
	360 : 'Motor 6 Recieved',
	361 : 'Motor 6 data',

	536 : 'Brake FR Recieved',
	537 : 'Brake FR data',
	536 : 'Brake FL Recieved',
	554 : 'Brake FL data',
	568 : 'Brake MR Recieved',
	569 : 'Brake MR data',
	584 : 'Brake ML Recieved',
	585 : 'Brake ML data',
	600 : 'Brake RR Recieved',
	601 : 'Brake RR data',
	616 : 'Brake RL Recieved',
	617 : 'Brake RL data',

	792 : 'Tensioner FR Recieved',
	793 : 'Tensioner FR data',
	807 : 'Tensioner FL Recieved',
	808 : 'Tensioner FL data',
	824 : 'Tensioner MR Recieved',
	825 : 'Tensioner MR data',
	840 : 'Tensioner ML Recieved',
	841 : 'Tensioner ML data',
	856 : 'Tensioner RR Recieved',
	857 : 'Tensioner RR data',
	872 : 'Tensioner RL Recieved',
	873 : 'Tensioner RL data',

	1048: 'LIDAR F Recieved',
	1049: 'LIDAR F data',
	1064: 'LIDAR R Recieved',
	1065: 'LIDAR R data',

	1304: 'BMS F Recieved',
	1320: 'BMS M Recieved',
	1336: 'BMS R Recieved',

	1305: 'BMS F data',
	1321: 'BMS M data',
	1337: 'BMS R data',

	1306: 'BMS arduino F data',
	1322: 'BMS arduino M data',
	1338: 'BMS arduino R data'
	}

# Append the reversed relationship (for two-way lookups)
ids.update(dict([[v,k] for k,v in ids.items()]))