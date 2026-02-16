# Instalar y cargar los paquetes necesarios
install.packages("mosaicData")  # Para los datos
install.packages("writexl")     # Para exportar a Excel

# Cargar los paquetes
library(mosaicData)
library(writexl)

# Cargar los datos
data(SaratogaHouses)

# Directorio
setwd("~/Analítica Estratégica de Datos en la Konrad/Machine Learning Probabilistico/Desarrollos ML/EDA")

# Exportar a CSV
write.csv(SaratogaHouses, "Input/saratoga_houses.csv", row.names = FALSE)

# Exportar a Excel
write_xlsx(SaratogaHouses, "Input/saratoga_houses.xlsx")

?SaratogaHouses
