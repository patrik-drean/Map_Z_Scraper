<h1 align="center" style="border-bottom: 3px solid #a8aeb7"> Map Z Scraper </h1>
A web scraping app that gathers data from a directory of households, exports the data to an xlsx file, compares and updates to the existing file, and then uploads the data to a mapping service called Zeemaps.com.

## Project Overview
**Language:** Python (Using the Selenium library) <br/>
**Team Members:** Patrik Drean<br/>

## Project Details
The project consists of 3 parts: <br/>

(1) Using Selenium, open a webbrowser, navigate to the URL, and scrape each household's information. Selenium had to be used over BeautifulSoup as AJAX is used for each individual household. <br/>
(2) Compare the updated households to the exisitng households. Zeemaps has an exported csv list of the households already on the map. The new households are compared to the current households. The result of the comparasion is exported to a new excel sheet, highlight households that will be added, ones that will be changed, and ones to be deleted (using the OpenPyxl library). <br/>
(3) Navigate to Zeemaps to delete all the households, followed by adding the current list of households. <br/>

## Lessons Learned 
<ul>  
  <li>Gained a deeper understanding how the Selenium, BeautifulSoup, and OpenPyxl libraries work by reading the docs and throughout the project. </li>
</ul>



