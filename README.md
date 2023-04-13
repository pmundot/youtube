# Youtube Data Analysis

This repository contains data and code for analyzing Youtube data from 11 countries: 
- Brazil 
- Canada 
- Denmark 
- France 
- Great Britain
- India
- Japan
- South Korea
- Mexico
- Russia 
- and United States. 
<br>The data is stored in the `youtube_data` folder as 11 csv files, each containing information such as video ID, title, publish date, channel ID and title, category, trending date, tags, view count, likes, dislikes, comment count, thumbnail link, and various flags indicating whether comments and ratings are disabled for a given video.

## File Structure

- `youtube_data`: folder containing csv files with Youtube data
- `Unit_testing.ipynb`: Jupyter notebook containing unit tests for the code
- `Youtube_Worldwide.ipynb`: Jupyter notebook containing analysis of Youtube data from all countries
- `Autolog.log`: log file containing errors from unit testing
- `Youtube_kernel.py`: Python script for running analysis on the data in the command line

## Libraries Required

The following libraries are required to run the code:

- `numpy`: for numerical operations
- `pandas`: for data manipulation and analysis
- `os`: for interacting with the operating system
- `glob`: for finding pathnames that match a specified pattern
- `sys`: for system-specific parameters and functions
- `matplotlib`: for creating visualizations
- `itertools`: for creating iterators for efficient looping
- `more_itertools`: for additional iterator functions
- `google_trans_new`: for translating text using Google Translate API
- `argparse`: for parsing command line arguments
- `logging`: for logging messages

You can install these libraries using pip:

```shell
pip install numpy pandas os glob sys matplotlib itertools more_itertools google_trans_new argparse logging
```


## Running the Code

To run the code, navigate to the repository directory in the command line and enter the following command:

```shell
python youtube_kernel.py print -g <grouping> -t <tags> -p <plot>
```

The `grouping` flag can take one of the following options:

- `Data`: Overall data
- `Country`: By country
- `Category`: By category
- `Country/category`: By country and category

The `tags` flag can take one of the following options:

- `Data`: All data
- `country`: Country abbreviations, such as `FR` for France.

The `plot` flag can take one of the following options:

- `Corr`: Correlation matrix
- `pie_tag`: Pie chart of tags used in each country
- `hist_tag`: Histogram of tags by country
- `pop`: Histogram of views per population

## License

This repository is licensed under the MIT License. Please refer to the LICENSE file for more information.
