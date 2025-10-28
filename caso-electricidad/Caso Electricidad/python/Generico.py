# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

class Extraccion_caracteristicas:
    
    def __init__(self, Data, Inicio, Final):
        self._data = Data
        self._inicio = Inicio
        self._final = Final
        
    def Sum(self):
        self._data['Sum'] = self._data.loc[:, self._inicio : self._final].sum(axis=1)
        
    def Mean(self):
        self._data['Mean'] = self._data.loc[:, self._inicio : self._final].mean(axis=1)
        
    def Median(self):
        self._data['Median'] = self._data.loc[:, self._inicio : self._final].median(axis=1)
        
    def Standard_Dev(self):
        self._data['Standard_Dev'] = self._data.loc[:, self._inicio : self._final].std(axis=1)
        
    def Variance(self):
        self._data['Variance'] = self._data.loc[:, self._inicio : self._final].var(axis=1)
        
    def Peak_to_Peak(self):
        self._data['Peak_to_Peak'] = list(np.ptp(np.array(self._data.loc[:, self._inicio : self._final]), axis=1))
        
    def Kurtosis(self):
        from scipy.stats import kurtosis
        self._data['Kurtosis'] = list(kurtosis(np.array(self._data.loc[:, self._inicio : self._final]), axis=1))
        
    def kstat(self):
        from scipy.stats import kstat
        self._data['kstat'] = list(kstat(np.array(self._data.loc[:, self._inicio : self._final]), axis=1))
        
    def KStatvar(self):
        from scipy.stats import kstatvar
        self._data['KStatvar'] = list(kstatvar(np.array(self._data.loc[:, self._inicio : self._final]), axis=1))
        
    def Quartile_1(self):
        self._data['Quartile_1'] = list(np.percentile(np.array(self._data.loc[:, self._inicio : self._final]), 25, axis=1))
        
    def Quartile_3(self):
        self._data['Quartile_3'] = list(np.percentile(np.array(self._data.loc[:, self._inicio : self._final]), 75, axis=1))
        
    def Norm(self):
        from scipy.linalg import norm
        self._data['Norm'] = list(norm(np.array(self._data.loc[:, self._inicio : self._final]), axis=1))
        
    def IQR(self):
        from scipy.stats import iqr
        self._data['IQR'] = list(iqr(np.array(self._data.loc[:, self._inicio : self._final]), axis=1))
        
    def Percentile_15(self):
        self._data['Percentile_15'] = list(np.percentile(np.array(self._data.loc[:, self._inicio : self._final]), 15, axis=1))
        
    def Percentile_65(self):
        self._data['Percentile_65'] = list(np.percentile(np.array(self._data.loc[:, self._inicio : self._final]), 65, axis=1))
        
    def Percentile_85(self):
        self._data['Percentile_85'] = list(np.percentile(np.array(self._data.loc[:, self._inicio : self._final]), 85, axis=1))
        
    def Median_Absolute_Deviation(self):
        from scipy.stats import median_abs_deviation
        self._data['Median_Absolute_Deviation'] = list(median_abs_deviation(np.array(self._data.loc[:, self._inicio : self._final]), axis=1))
        
class Graficos():
    def __init__(self, df):
        self._df = df
        
    def Correlacion(self, method, TipoGrafico: int):
        import pandas as pd
        import seaborn as sns
        from matplotlib import pyplot as plt
        
        if TipoGrafico == 0:
            corr = self._df.corr(method)*100
            return corr
        
        elif TipoGrafico == 1:
            h_labels = [x.replace('_', ' ').title() 
                        for x in list(self._df.select_dtypes(
                                include=['number', 'bool']).columns.values)
                        ]
    
            fig, ax = plt.subplots(figsize=(15,6))
            _ = sns.heatmap(
            self._df.corr(method), 
            annot=True, 
            xticklabels=h_labels, 
            yticklabels=h_labels, 
            cmap=sns.cubehelix_palette(as_cmap=True), ax=ax)
            
        elif TipoGrafico== 2:
            corr = self._df.corr(method)
            plt.figure(figsize=(15, 6))
            ax = sns.heatmap(
                corr, 
                vmin=-1, vmax=1, center=0,
                cmap=sns.diverging_palette(20, 220, n=200),
                square=True
)
            
    def calcular_correlacion(self, columna, cantidad_columnas, tipo_retorno):
        # Verificar si la columna especificada existe en el DataFrame
        if columna not in self._df.columns:
            return f"La columna '{columna}' no existe en el DataFrame."

        correlaciones = self._df.corr()

        if tipo_retorno == "alta corr":
            correlaciones_ord = correlaciones[columna].sort_values(ascending=False)
        elif tipo_retorno == "baja corr":
            correlaciones_ord = correlaciones[columna].sort_values(ascending=True)
        else:
            return "Tipo de retorno no válido"

        # Excluir la correlación con la misma columna
        correlaciones_ord = correlaciones_ord.drop(columna)
        
        columnas_seleccionadas = correlaciones_ord.head(cantidad_columnas).index.tolist()
        
        return columnas_seleccionadas
        
    def BoxPlot(self, Caracteristica, limite:str):
        from matplotlib import pyplot as plt
        import seaborn as sns
        
        
        if limite == 'Ninguno':
            plt.figure(figsize=(6, 5))
            sns.boxplot(
                data=self._df,
                x = 'FLAG',
                y= Caracteristica
            )
            
        elif limite == 'General':
            _desc = self._df.describe()

            Q3_s = _desc.loc['75%', Caracteristica]
            Q1_s = _desc.loc['25%', Caracteristica]
            IQR_s =  Q3_s - Q1_s
            Bigote_Superior = Q3_s + (1.5 * IQR_s)
            Bigote_Inferior = Q1_s - (1.5 * IQR_s)

            print(f"""
            Q1: {Q1_s}
            Q3: {Q3_s}
            IQR: {IQR_s}
            Bigote Superior: {Bigote_Superior}
            Bigote Inferior: {Bigote_Inferior}
            \n""")
            
            plt.figure(figsize=(6, 5))
            sns.boxplot(
                data=self._df[self._df[Caracteristica] <= Bigote_Superior],
                x = 'FLAG',
                y= Caracteristica
            )

        elif limite == 'FLAG = 0':
            _desc = self._df.query('FLAG == 0').describe()

            Q3_s = _desc.loc['75%', Caracteristica]
            Q1_s = _desc.loc['25%', Caracteristica]
            IQR_s =  Q3_s - Q1_s
            Bigote_Superior = Q3_s + (1.5 * IQR_s)
            Bigote_Inferior = Q1_s + (1.5 * IQR_s)

            print(f"""
            Q1: {Q1_s}
            Q3: {Q3_s}
            IQR: {IQR_s}
            Bigote Superior: {Bigote_Superior}
            Bigote Inferior: {Bigote_Inferior}
            \n""")
            
            plt.figure(figsize=(6, 5))
            sns.boxplot(
                data=self._df[self._df[Caracteristica] <= Bigote_Superior],
                x = 'FLAG',
                y= Caracteristica
            )
            
        elif limite == 'FLAG = 1':
            _desc = self._df.query('FLAG == 1').describe()

            Q3_s = _desc.loc['75%', Caracteristica]
            Q1_s = _desc.loc['25%', Caracteristica]
            IQR_s =  Q3_s - Q1_s
            Bigote_Superior = Q3_s + (1.5 * IQR_s)
            Bigote_Inferior = Q1_s + (1.5 * IQR_s)

            print(f"""
            Q1: {Q1_s}
            Q3: {Q3_s}
            IQR: {IQR_s}
            Bigote Superior: {Bigote_Superior}
            Bigote Inferior: {Bigote_Inferior}
            \n""")
            
            plt.figure(figsize=(6, 5))
            sns.boxplot(
                data=self._df[self._df[Caracteristica] <= Bigote_Superior],
                x = 'FLAG',
                y= Caracteristica
            )