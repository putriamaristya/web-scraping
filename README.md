# Web scraping: extracting medicine details from BPOM's website

## Introduction
This script extracts medicine details from BPOM's website using Selenium on Python. 

## Requirements
  - Python 3.11.9
  - Selenium 4.25.0
  - Pandas 1.5.3

## Website
The website that is 'scraped' in this script is [cekbpom.pom.go.id/obat](cekbpom.pom.go.id/obat). This script is suitable for the version of the website accessed on October 2nd 2024, 18.49 (GMT+7).

## Details
When you open [cekbpom.pom.go.id/obat](cekbpom.pom.go.id/obat) and click on a medicine name, you will see the details of the medicine. This script 'clicks' on each medicine and extracts its details. The details extracted include:
  - kode_registrasi	
  - tanggal_terbit	
  - masa_berlaku	
  - diterbitkan_oleh	
  - nama_produk	
  - bentuk_sediaan	
  - merk	
  - kemasan	
  - pendaftar	
  - diproduksi_oleh
  
## Output
The output is an excel sheet where columns consist of the extracted details and rows consist of the medicines. 

## Notes
  - The number of pages extracted is hard coded in the script. You can adjust this accordingly on line 100. So far, the script has been used to extract up to 10 pages of the website. 
  - Your internet connection has to be somewhat good and fast. If you don't, you can try adjusting the time.sleep() parameter on line 19 and line 34. You can also try adjusting the time.sleep() if the script breaks abruptly
  - If the website changes design or anything, the script may not work