<?php

require('../config/db_config.php');
$db_link = mysqli_connect($db_server, $db_username, $db_password, $db_database);
if (mysqli_connect_errno($db_link)) {
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
}


if (($handle = fopen("Chicago_USACE_01.16.14.csv", "r")) !== FALSE) {
	$taxa_inserted = 0;
	$taxa_updated = 0;
	$rows_inserted = '';
	while (($data = fgetcsv($handle, 0, ",", '"')) !== FALSE) {

		// skip the header row
		if (trim(strtolower($data[0])) !== "scientific name") {
			//scientific name, family, acronym, nativity, coefficient of conservatism, coefficient of wetness, physiognomy, duration, common name
			$scientific_name = mysqli_real_escape_string($db_link, ucfirst(strtolower(trim($data[0]))));
			$family = mysqli_real_escape_string($db_link, ucfirst(strtolower(trim($data[1]))));
			$acronym = mysqli_real_escape_string($db_link, strtoupper(trim($data[2])));
			$native = mysqli_real_escape_string($db_link, strtolower(trim($data[3])));
			$c_o_c = mysqli_real_escape_string($db_link, trim($data[4]));
			$c_o_w = mysqli_real_escape_string($db_link, trim($data[5]));
			$physiognomy = mysqli_real_escape_string($db_link, strtolower(trim($data[6])));
			$duration = mysqli_real_escape_string($db_link, strtolower(trim($data[7])));
			$common_name = mysqli_real_escape_string($db_link, strtolower(trim($data[8])));
			// remove any quotes (typically in common names e.g. "Witch's Teeth Lotus")
			$scientific_name = str_replace("'", "", $scientific_name);
			$family = str_replace("'", "", $family);
			$common_name = str_replace("'", "", $common_name);
			// check that scientific name has been entered
			if (strlen($scientific_name) < 4) {
				$result = "Error: Please enter a valid scientific name. See line #".$taxa_inserted;
				break;
			}
			// check that c_o_c and c_o_w are integers
			if (!is_numeric( $c_o_c ) || ($c_o_c < 0) || (10 < $c_o_c)) {
				$result = "Error: The coefficient of conservatism must be an integer from 0-10. See line #".$taxa_inserted;
				break;
			}
			if (($c_o_w !== '') && (!is_numeric( $c_o_w ) || ($c_o_w < -5) || (5 < $c_o_w))) {
				$result = "Error: The coefficient of wetness must be an integer between -5 and 5. See line #".$taxa_inserted;
				break;
			}
			// check native/non-native
			if ($native !== 'native' && $native !== 'non-native') {
				$result = "Error: The column native must be either 'native' or 'non-native'. See line #".$taxa_inserted;
				break;
			}
			if ($native == 'native')
				$native = 1;
			if ($native == 'non-native')
				$native = 0;
			// check physiognomy "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
			if (($physiognomy !== '') && ($physiognomy !== 'fern' && $physiognomy !== 'forb' && $physiognomy !== 'grass' && $physiognomy !== 'rush' && $physiognomy !== 'sedge' && $physiognomy !== 'shrub' && $physiognomy !== 'tree' && $physiognomy !== 'vine' && $physiognomy !== 'bryophyte')) {
				$result = "Error: Please enter a valid term for physiognomy. See line #".$taxa_inserted;
				break;
			}
			// check duration  "annual", "biennial", or "perennial"
			if (($duration !== '') && ($duration !== 'annual' && $duration !== 'biennial' && $duration !== 'perennial')) {
				$result = "Error: Please enter a valid term for duration (either annual, biennial, or perennial). See line #".$taxa_inserted;
				break;
			}
			if ($family == '')
				$family = null;
			if ($acronym == '')
				$acronym = null;
			if ($common_name == '')
				$common_name = null;
			if ($c_o_w == '')
				$c_o_w = null;
			if ($physiognomy == '')
				$physiognomy = null;
			if ($duration == '')
				$duration = null;

			//$scientific_name = str_replace(' ;', ';', $scientific_name);

			// do not insert if there is already a taxa with this sci name for this fqa db
			$found = false;
			$sql = "SELECT * FROM taxa WHERE scientific_name LIKE '%$scientific_name%' AND fqa_id='9'";
			$existing_taxa = mysqli_query($db_link, $sql);
			if (mysqli_num_rows($existing_taxa) > 0) {
				$found = true;
			} else {
				// hack to fix the awful non-ascii characters
				$scientific_name2 = str_replace('_', 'fl', $scientific_name);
				$sql = "SELECT * FROM taxa WHERE scientific_name LIKE '%$scientific_name2%' AND fqa_id='9'";
				$existing_taxa = mysqli_query($db_link, $sql);
				if (mysqli_num_rows($existing_taxa) > 0) {
					$scientific_name = $scientific_name2;
					$found = true;
				} else {
					$scientific_name2 = str_replace('_', 'fi', $scientific_name);
					$sql = "SELECT * FROM taxa WHERE scientific_name LIKE '%$scientific_name2%' AND fqa_id='9'";
					$existing_taxa = mysqli_query($db_link, $sql);
					if (mysqli_num_rows($existing_taxa) > 0) {
						$scientific_name = $scientific_name2;
						$found = true;
					} else {
						$scientific_name2 = str_replace('_', 'f', $scientific_name);
						$sql = "SELECT * FROM taxa WHERE scientific_name LIKE '%$scientific_name2%' AND fqa_id='9'";
						$existing_taxa = mysqli_query($db_link, $sql);
						if (mysqli_num_rows($existing_taxa) > 0) {
							$scientific_name = $scientific_name2;
							$found = true;
						}
					}
				}
			}
			if (!$found) {
				// avoid mysql int = null = 0 problem
				if ($c_o_w == null)
					$sql = "INSERT INTO taxa (fqa_id, scientific_name, family, common_name, acronym, c_o_c, native, physiognomy, duration) VALUES ('$fqa_id', '$scientific_name', '$family', '$common_name', '$acronym', '$c_o_c', '$native', '$physiognomy', '$duration')";
				else
					$sql = "INSERT INTO taxa (fqa_id, scientific_name, family, common_name, acronym, c_o_c, c_o_w, native, physiognomy, duration) VALUES ('$fqa_id', '$scientific_name', '$family', '$common_name', '$acronym', '$c_o_c', '$c_o_w', '$native', '$physiognomy', '$duration')";					
				// mysqli_query($db_link, $sql);
				$taxa_inserted++;

				$rows_inserted = $rows_inserted . "<br>" . $scientific_name;
			} else {
				// update the existing
				$sql = "UPDATE taxa SET acronym='$acronym' WHERE scientific_name LIKE '%$scientific_name%' AND fqa_id='9'";
				// mysqli_query($db_link, $sql);
				$taxa_updated++;
			}
		}
	}
	if ($result == "") {
		echo $rows_inserted . "<br><br>";
		echo "Inserted " . $taxa_inserted . " new taxa.";
		echo "Updated " . $taxa_updated . " taxa.";
	} else {
		echo $result;
	
	}

}
mysqli_close($db_link);

?>
