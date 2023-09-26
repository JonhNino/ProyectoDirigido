# analisis expliratorio de datos #
#------cargando librerias---------

install.packages("openxlsx")
install.packages("opencsv")
library(opencsv)
library(openxlsx)                   # se usa para poder cargar bases de datos de exel
install.packages("ggthemes")
library(ggthemes)                   # se usa para dar formato a los graficos en 
install.packages("ggplot2")
library(ggplot2)                     # 
install.packages("DataExplorer")    #
library(DataExplorer)
install.packages("readr")

#----------------carga de datos------------------

file.choose()

datos <- read.csv2("D:/PosgradosII/MODULO_BODEGA_DE_DATOS/datos proyecto/ARS_USD.csv")
datos2 <- read.csv2("D:\\PosgradosII\\MODULO_BODEGA_DE_DATOS\\datos proyecto\\BOB_USD.csv")

#----------------ploteo basico-------------------

str(datos)
head(datos)

plot(datos$dep.vista)


