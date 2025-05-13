<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

# VITALS

<em>Record and visualise your health data.</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/jackwoodman/vitals?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
<img src="https://img.shields.io/github/last-commit/jackwoodman/vitals?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/jackwoodman/vitals?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/jackwoodman/vitals?style=default&color=0080ff" alt="repo-language-count">

<!-- default option, no dependency badges. -->


<!-- default option, no dependency badges. -->

</div>
<br>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
    - [Project Index](#project-index)
---

## Overview

**vitals**

The core features include:

- **🚀 Interactive Data Visualization:** Utilise Plotly for visually engaging data representation.
- **🔍 Efficient Metric Management:** Streamline health metric organization and analysis.
- **💻 User-Friendly CLI Displays:** Enhance user interaction with intuitive command line interfaces.
- **📝 Automated Log Management:** Easily track and manage log entries for record-keeping.



---
## Project Structure

```sh
└── vitals/
    ├── README.md
    ├── classes.py
    ├── data
    │   ├── analysis_tools.py
    │   └── data_entry.py
    ├── file_tools
    │   ├── filepaths.py
    │   ├── metric_file_parsing.py
    │   └── utils.py
    ├── global_functions.py
    ├── high_level_functions
    │   ├── analyse.py
    │   ├── entry_points.py
    │   ├── graph.py
    │   ├── manage.py
    │   ├── read.py
    │   ├── utils.py
    │   └── write.py
    ├── main.py
    ├── requirements.txt
    ├── txt_files
    │   ├── feature_wishlist.txt
    │   └── health_file_update_log.txt
    └── utils
        ├── cli_displays.py
        ├── deprecated_functions.py
        ├── logger.py
        ├── plotting.py
        ├── sequence_matcher.py
        └── utils.py
```

### Project Index

<details open>
	<summary><b><code>VITALS/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/requirements.txt'>requirements.txt</a></b></td>
					<td style='padding: 8px;'>Enable interactive data visualization using Plotly in the project.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/global_functions.py'>global_functions.py</a></b></td>
					<td style='padding: 8px;'>- Initialize the GroupManager with aliases from a JSON file, utilizing functions to ingest and manage health metrics<br>- The code facilitates registering and deregistering metric groups, providing a robust system for organizing and handling health data within the project architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/classes.py'>classes.py</a></b></td>
					<td style='padding: 8px;'>- Define and manage health metrics, measurements, and groups within the project architecture<br>- Capture and analyze data for various metric types, such as ranged, greater than, less than, and boolean<br>- Utilize classes to structure and organize metric data effectively for visualization and analysis.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/main.py'>main.py</a></b></td>
					<td style='padding: 8px;'>- Define a high-level loop to map commands to functions, facilitating user interaction and command execution<br>- The loop orchestrates key functions like write, read, graph, manage, analyse, and memorise, enhancing the programs usability<br>- It also ensures a smooth user experience by handling interruptions gracefully.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- txt_files Submodule -->
	<details>
		<summary><b>txt_files</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ txt_files</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/txt_files/health_file_update_log.txt'>health_file_update_log.txt</a></b></td>
					<td style='padding: 8px;'>Update health file to support various data types and units, enhancing usability and data integrity.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/txt_files/feature_wishlist.txt'>feature_wishlist.txt</a></b></td>
					<td style='padding: 8px;'>- Enhances metric management by reading, updating, and creating metric files<br>- Adds functionality for correctness checks, mass updates, out-of-range searches, and spellchecks<br>- Enables graphing multiple metrics and organizing data efficiently within the project structure.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- utils Submodule -->
	<details>
		<summary><b>utils</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ utils</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/utils/cli_displays.py'>cli_displays.py</a></b></td>
					<td style='padding: 8px;'>Pad titles with buffer characters, display a welcome graphic, and prompt users for input based on the current program level.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/utils/deprecated_functions.py'>deprecated_functions.py</a></b></td>
					<td style='padding: 8px;'>- Enhances plot visualization by adding lines and shading based on metric data<br>- Dynamically creates y-axes for each line, accommodating various object types like ranged, greater than, and less than<br>- Updates the layout with new y-axes as needed, improving the clarity and depth of the plotted metrics.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/utils/plotting.py'>plotting.py</a></b></td>
					<td style='padding: 8px;'>- Generate interactive and visually appealing plots for multiple health metrics, each with its own y-axis<br>- Easily visualize data with ideal bounds displayed<br>- The code efficiently organizes metrics on the graph, ensuring clarity and distinction between different units.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/utils/logger.py'>logger.py</a></b></td>
					<td style='padding: 8px;'>- LogCollector class manages log entries, allowing addition, counting, and dumping to a file<br>- It ensures logs are stored and can be output to a file for record-keeping<br>- The class also supports different log levels and formats entries for easy readability.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/utils/utils.py'>utils.py</a></b></td>
					<td style='padding: 8px;'>- Implement a function to recursively flatten nested lists into a single array<br>- Additionally, define a generic interface function for handling High-Level Language (HLL) operations, promoting code reusability<br>- Lastly, include a utility function to ingest health metrics from files, providing flexibility for user input and verbose output.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/utils/sequence_matcher.py'>sequence_matcher.py</a></b></td>
					<td style='padding: 8px;'>- Implement functions to find and return the closest matching strings from a list based on a candidate string<br>- The functions sort possible strings by similarity to the candidate string and return the closest matches.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- file_tools Submodule -->
	<details>
		<summary><b>file_tools</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ file_tools</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/file_tools/utils.py'>utils.py</a></b></td>
					<td style='padding: 8px;'>Create a directory if not existing and check for inequality values in strings.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/file_tools/metric_file_parsing.py'>metric_file_parsing.py</a></b></td>
					<td style='padding: 8px;'>- Generate, write, and manage health metric files with ease using the provided code<br>- Effortlessly read, write, update, and rename metric files, ensuring data integrity and accuracy<br>- Simplify the process of handling health metrics by leveraging the functions within this code file.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/file_tools/filepaths.py'>filepaths.py</a></b></td>
					<td style='padding: 8px;'>Retrieve a list of filenames without extensions from a specified directory.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- high_level_functions Submodule -->
	<details>
		<summary><b>high_level_functions</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ high_level_functions</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/high_level_functions/analyse.py'>analyse.py</a></b></td>
					<td style='padding: 8px;'>Analyze data to derive insights and trends, enhancing decision-making within the projects architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/high_level_functions/write.py'>write.py</a></b></td>
					<td style='padding: 8px;'>- Facilitates user input for writing new measurements and metrics within the projects data entry mode<br>- Handles different input modes such as manual, assisted, and speedy, allowing users to select the appropriate handler<br>- The code initiates an input loop, guiding users through the process while ensuring data integrity and accuracy.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/high_level_functions/graph.py'>graph.py</a></b></td>
					<td style='padding: 8px;'>- Generate visual health metric plots from requested data files using global functions and plotting utilities<br>- Read data, create plots based on the number of metrics, and display the visualizations with optional bounds.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/high_level_functions/entry_points.py'>entry_points.py</a></b></td>
					<td style='padding: 8px;'>- Define high-level functions for managing, analyzing, graphing, reading, writing, and memorizing data<br>- These functions serve as entry points to interact with the core functionalities of the project, enabling users to perform various data operations efficiently.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/high_level_functions/utils.py'>utils.py</a></b></td>
					<td style='padding: 8px;'>- Generates and updates a group manager file with health metric data, saving it to a specified directory<br>- Handles file writing errors and logs actions<br>- Also includes a function to exit the high-level loop, updating the group manager file and logging program termination.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/high_level_functions/manage.py'>manage.py</a></b></td>
					<td style='padding: 8px;'>- Manage.py facilitates metric file management within the project<br>- It offers functions to rename, display, search, update units, and instantiate new health metric files<br>- These operations streamline the handling of metric data, enhancing efficiency in managing and updating metrics for the project.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/jackwoodman/vitals/blob/master/high_level_functions/read.py'>read.py</a></b></td>
					<td style='padding: 8px;'>- Reads and displays health metrics from a specified file<br>- Handles loading and presenting metric data in a structured format<br>- Parses the file content into HealthMetric objects and prints associated entries for each metric<br>- Handles cases where no data is found in the provided file.</td>
				</tr>
			</table>
		</blockquote>
	</details>
</details>

---
