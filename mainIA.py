"""
Módulo de Análise e Engenharia de Dados - CEP e Renda Per Capita
================================================================
Este módulo realiza o processamento, limpeza, transformação e visualização
de dados de CEPs brasileiros com informações de renda per capita.

Autor: Tiago
Data: 2026
"""

import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configurações de visualização
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


# ============================================================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================================================

@dataclass(frozen=True)
class Config:
    """Configurações globais do projeto."""
    ARQUIVO_DADOS: str = 'cep_coordinates_per_capita_income.csv'
    COLUNAS_REMOVER: Tuple[str, ...] = ("CD_GEOCODI", "LON", "LAT")
    FIGSIZE_PADRAO: Tuple[int, int] = (12, 6)
    LIMITE_RENDA_ZOOM: int = 3000


# Mapeamento de regiões por primeiro dígito do CEP
MAPA_REGIOES: Dict[str, str] = {
    '0': 'Grande São Paulo',
    '1': 'Interior SP / Santos',
    '2': 'Rio de Janeiro / ES',
    '3': 'Minas Gerais',
    '4': 'Bahia / Sergipe',
    '5': 'PE / AL / PB / RN',
    '6': 'CE / PI / MA / PA / AP / AM',
    '7': 'DF / GO / TO / MT / MS / RO',
    '8': 'PR / SC',
    '9': 'RS'
}

# Limites de CEP por estado (para classificação)
LIMITES_CEP: List[int] = [
    -1, 19999999, 28999999, 29999999, 39999999, 48999999, 49999999, 
    56999999, 57999999, 58999999, 59999999, 63999999, 64999999, 
    65999999, 68899999, 68999999, 69299999, 69399999, 69899999, 
    69999999, 72799999, 72999999, 73699999, 76799999, 76999999, 
    77999999, 78899999, 79999999, 87999999, 89999999, 99999999
]

ESTADOS: List[str] = [
    "SP", "RJ", "ES", "MG", "BA", "SE", "PE", "AL", "PB", "RN", 
    "CE", "PI", "MA", "PA", "AP", "AM", "RR", "AM", "AC", "DF", 
    "GO", "DF", "GO", "RO", "TO", "MT", "MS", "PR", "SC", "RS"
]


# ============================================================================
# CLASSE PRINCIPAL DE ENGENHARIA DE DADOS
# ============================================================================

class EngenhariaDados:
    """
    Classe responsável pela carga, limpeza e transformação dos dados.
    
    Attributes:
        dados: DataFrame com os dados carregados
        label_encoders: Dicionário com os encoders utilizados
    """
    
    def __init__(self, arquivo: Optional[str] = None):
        """
        Inicializa a classe de engenharia de dados.
        
        Args:
            arquivo: Caminho do arquivo CSV (opcional)
        """
        self.dados: Optional[pd.DataFrame] = None
        self.dados_originais: Optional[pd.DataFrame] = None
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self._estatisticas: Dict = {}
        
        if arquivo:
            self.carregar_arquivo(arquivo)
    
    def carregar_arquivo(self, nome_arquivo: str) -> Optional[pd.DataFrame]:
        """
        Carrega um arquivo CSV de forma segura.
        
        Args:
            nome_arquivo: Nome ou caminho do arquivo CSV
            
        Returns:
            DataFrame carregado ou None em caso de erro
        """
        logger.info(f"Iniciando carga do arquivo: {nome_arquivo}")
        
        caminho = Path(nome_arquivo)
        
        if not caminho.exists():
            logger.error(f"Arquivo não encontrado: {nome_arquivo}")
            return None
        
        try:
            self.dados = pd.read_csv(nome_arquivo)
            self.dados_originais = self.dados.copy()
            
            logger.info(f"Arquivo carregado com sucesso!")
            logger.info(f"  → Registros: {len(self.dados):,}")
            logger.info(f"  → Colunas: {list(self.dados.columns)}")
            
            return self.dados
            
        except pd.errors.EmptyDataError:
            logger.error("O arquivo está vazio")
        except pd.errors.ParserError as e:
            logger.error(f"Erro ao parsear o arquivo: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao carregar arquivo: {e}")
        
        return None
    
    def limpar_dados(self) -> 'EngenhariaDados':
        """
        Realiza a limpeza básica dos dados.
        
        Returns:
            self para permitir encadeamento de métodos
        """
        if self.dados is None:
            logger.warning("Nenhum dado carregado para limpar")
            return self
        
        logger.info("Iniciando limpeza dos dados...")
        
        # Registros antes da limpeza
        registros_inicial = len(self.dados)
        
        # Remover duplicatas
        duplicatas = self.dados.duplicated().sum()
        self.dados.drop_duplicates(inplace=True)
        logger.info(f"  → Duplicatas removidas: {duplicatas}")
        
        # Remover valores nulos
        nulos = self.dados.isnull().sum().sum()
        self.dados.dropna(inplace=True)
        logger.info(f"  → Registros com nulos removidos: {nulos}")
        
        # Remover registros sem CEP válido
        if 'POSTCODE' in self.dados.columns:
            sem_cep = len(self.dados[self.dados['POSTCODE'] == 'Sem CEP'])
            self.dados = self.dados[self.dados['POSTCODE'] != 'Sem CEP']
            logger.info(f"  → Registros 'Sem CEP' removidos: {sem_cep}")
        
        registros_final = len(self.dados)
        logger.info(f"  → Total removido: {registros_inicial - registros_final} registros")
        logger.info(f"  → Registros restantes: {registros_final:,}")
        
        return self
    
    def remover_colunas(self, colunas: Tuple[str, ...] = Config.COLUNAS_REMOVER) -> 'EngenhariaDados':
        """
        Remove colunas especificadas do DataFrame.
        
        Args:
            colunas: Tupla com nomes das colunas a remover
            
        Returns:
            self para permitir encadeamento de métodos
        """
        if self.dados is None:
            return self
        
        colunas_existentes = [col for col in colunas if col in self.dados.columns]
        
        if colunas_existentes:
            self.dados.drop(columns=colunas_existentes, inplace=True)
            logger.info(f"Colunas removidas: {colunas_existentes}")
        
        return self
    
    def criar_features(self) -> 'EngenhariaDados':
        """
        Cria novas features a partir dos dados existentes.
        
        Returns:
            self para permitir encadeamento de métodos
        """
        if self.dados is None:
            return self
        
        logger.info("Criando novas features...")
        
        # Feature: Região baseada no primeiro dígito do CEP
        self.dados['Regiao'] = self.dados['POSTCODE'].str[0].map(MAPA_REGIOES)
        logger.info("  → Feature 'Regiao' criada")
        
        # Feature: CEP numérico (sem hífen)
        self.dados['cep_numerico'] = (
            self.dados['POSTCODE']
            .str.replace(r'\D', '', regex=True)
            .astype('int32')
        )
        logger.info("  → Feature 'cep_numerico' criada")
        
        # Feature: Estado (UF) baseado no CEP
        self.dados['UF'] = pd.cut(
            self.dados['cep_numerico'], 
            bins=LIMITES_CEP, 
            labels=ESTADOS, 
            right=True, 
            ordered=False
        )
        logger.info("  → Feature 'UF' criada")
        
        # Feature: Tipo (Capital vs Interior) - CEPs terminados em 000 são geralmente capitais
        self.dados['Tipo'] = np.where(
            self.dados['cep_numerico'] % 1000 == 0, 
            'Capital', 
            'Interior'
        )
        logger.info("  → Feature 'Tipo' criada")
        
        # Feature: Faixa de renda
        self.dados['Faixa_Renda'] = pd.cut(
            self.dados['renda_per_capita'],
            bins=[0, 300, 500, 800, 1000, float('inf')],
            labels=['Muito Baixa', 'Baixa', 'Média', 'Alta', 'Muito Alta']
        )
        logger.info("  → Feature 'Faixa_Renda' criada")
        
        return self
    
    def codificar_categoricas(self, colunas: Optional[List[str]] = None) -> 'EngenhariaDados':
        """
        Codifica colunas categóricas usando LabelEncoder.
        
        Args:
            colunas: Lista de colunas para codificar (default: Regiao e UF)
            
        Returns:
            self para permitir encadeamento de métodos
        """
        if self.dados is None:
            return self
        
        colunas = colunas or ['Regiao', 'UF']
        
        logger.info("Codificando variáveis categóricas...")
        
        for coluna in colunas:
            if coluna in self.dados.columns:
                # Criar coluna codificada preservando a original
                encoder = LabelEncoder()
                self.dados[f'{coluna}_cod'] = encoder.fit_transform(
                    self.dados[coluna].astype(str)
                )
                self.label_encoders[coluna] = encoder
                logger.info(f"  → Coluna '{coluna}' codificada → '{coluna}_cod'")
        
        return self
    
    def gerar_estatisticas(self) -> Dict:
        """
        Gera estatísticas resumidas dos dados.
        
        Returns:
            Dicionário com estatísticas
        """
        if self.dados is None:
            return {}
        
        logger.info("\n" + "="*60)
        logger.info("ESTATÍSTICAS DO DATASET")
        logger.info("="*60)
        
        self._estatisticas = {
            'total_registros': len(self.dados),
            'total_colunas': len(self.dados.columns),
            'colunas': list(self.dados.columns),
            'tipos_dados': self.dados.dtypes.to_dict(),
            'valores_unicos': self.dados.nunique().to_dict(),
            'memoria_mb': self.dados.memory_usage(deep=True).sum() / 1024**2
        }
        
        logger.info(f"Total de registros: {self._estatisticas['total_registros']:,}")
        logger.info(f"Total de colunas: {self._estatisticas['total_colunas']}")
        logger.info(f"Uso de memória: {self._estatisticas['memoria_mb']:.2f} MB")
        
        # Estatísticas da renda per capita
        if 'renda_per_capita' in self.dados.columns:
            renda_stats = self.dados['renda_per_capita'].describe()
            self._estatisticas['renda'] = renda_stats.to_dict()
            logger.info(f"\nEstatísticas de Renda Per Capita:")
            logger.info(f"  → Média: R$ {renda_stats['mean']:.2f}")
            logger.info(f"  → Mediana: R$ {renda_stats['50%']:.2f}")
            logger.info(f"  → Desvio Padrão: R$ {renda_stats['std']:.2f}")
            logger.info(f"  → Mínimo: R$ {renda_stats['min']:.2f}")
            logger.info(f"  → Máximo: R$ {renda_stats['max']:.2f}")
        
        return self._estatisticas
    
    def analisar_variacao_renda(self, top_n: int = 5) -> pd.Series:
        """
        Analisa a variação de renda por região.
        
        Args:
            top_n: Número de regiões para exibir
            
        Returns:
            Series com desvio padrão por região
        """
        if self.dados is None or 'Regiao' not in self.dados.columns:
            return pd.Series()
        
        desvio_renda = (
            self.dados
            .groupby('Regiao')['renda_per_capita']
            .std()
            .sort_values(ascending=False)
        )
        
        logger.info(f"\nTop {top_n} regiões com maior variação de renda:")
        for i, (regiao, desvio) in enumerate(desvio_renda.head(top_n).items(), 1):
            logger.info(f"  {i}. {regiao}: R$ {desvio:.2f}")
        
        return desvio_renda
    
    def processar_pipeline(self) -> pd.DataFrame:
        """
        Executa o pipeline completo de processamento de dados.
        
        Returns:
            DataFrame processado
        """
        logger.info("\n" + "="*60)
        logger.info("INICIANDO PIPELINE DE PROCESSAMENTO")
        logger.info("="*60 + "\n")
        
        return (
            self
            .limpar_dados()
            .remover_colunas()
            .criar_features()
            .codificar_categoricas()
            .gerar_estatisticas()
        )
    
    def obter_dados(self) -> Optional[pd.DataFrame]:
        """Retorna o DataFrame processado."""
        return self.dados


# ============================================================================
# CLASSE DE VISUALIZAÇÃO DE DADOS
# ============================================================================

class VisualizacaoDados:
    """
    Classe responsável pela visualização e análise gráfica dos dados.
    
    Attributes:
        dados: DataFrame com os dados para visualização
        figsize: Tamanho padrão das figuras
    """
    
    def __init__(self, dados: pd.DataFrame, figsize: Tuple[int, int] = Config.FIGSIZE_PADRAO):
        """
        Inicializa a classe de visualização.
        
        Args:
            dados: DataFrame com os dados processados
            figsize: Tupla com (largura, altura) das figuras
        """
        self.dados = dados
        self.figsize = figsize
        self._configurar_estilo()
    
    def _configurar_estilo(self) -> None:
        """Configura o estilo padrão dos gráficos."""
        plt.rcParams['figure.figsize'] = self.figsize
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
    
    def grafico_barras_renda_regiao(self, mostrar: bool = True) -> plt.Figure:
        """
        Cria gráfico de barras da média de renda por região.
        
        Args:
            mostrar: Se True, exibe o gráfico imediatamente
            
        Returns:
            Objeto Figure do matplotlib
        """
        media_renda = (
            self.dados
            .groupby('Regiao')['renda_per_capita']
            .mean()
            .sort_values(ascending=True)
        )
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        bars = ax.barh(media_renda.index, media_renda.values, color=plt.cm.viridis(
            np.linspace(0.2, 0.8, len(media_renda))
        ))
        
        # Adicionar valores nas barras
        for bar, valor in zip(bars, media_renda.values):
            ax.text(valor + 10, bar.get_y() + bar.get_height()/2, 
                   f'R$ {valor:.0f}', va='center', fontsize=9)
        
        ax.set_xlabel('Renda Per Capita Média (R$)')
        ax.set_title('Média de Renda Per Capita por Região', fontweight='bold')
        ax.set_xlim(0, media_renda.max() * 1.15)
        
        plt.tight_layout()
        
        if mostrar:
            plt.show()
        
        return fig
    
    def grafico_pizza_distribuicao(self, mostrar: bool = True) -> plt.Figure:
        """
        Cria gráfico de pizza da distribuição de renda por região.
        
        Args:
            mostrar: Se True, exibe o gráfico imediatamente
            
        Returns:
            Objeto Figure do matplotlib
        """
        media_renda = self.dados.groupby('Regiao')['renda_per_capita'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(media_renda)))
        
        wedges, texts, autotexts = ax.pie(
            media_renda.values, 
            labels=media_renda.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=[0.02] * len(media_renda),
            shadow=True
        )
        
        # Melhorar legibilidade
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        
        ax.set_title('Distribuição da Renda Média por Região', fontweight='bold', size=14)
        ax.axis('equal')
        
        plt.tight_layout()
        
        if mostrar:
            plt.show()
        
        return fig
    
    def grafico_barras_renda_estado(self, mostrar: bool = True) -> plt.Figure:
        """
        Cria gráfico de barras da média de renda por estado (UF).
        
        Args:
            mostrar: Se True, exibe o gráfico imediatamente
            
        Returns:
            Objeto Figure do matplotlib
        """
        media_renda = (
            self.dados
            .groupby('UF')['renda_per_capita']
            .mean()
            .sort_values(ascending=False)
        )
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(media_renda)))
        
        bars = ax.bar(media_renda.index.astype(str), media_renda.values, color=colors)
        
        ax.axhline(y=media_renda.mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Média Nacional: R$ {media_renda.mean():.0f}')
        
        ax.set_xlabel('Estado (UF)')
        ax.set_ylabel('Renda Per Capita Média (R$)')
        ax.set_title('Média de Renda Per Capita por Estado', fontweight='bold')
        ax.legend()
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if mostrar:
            plt.show()
        
        return fig
    
    def grafico_linha_desvio_renda(self, mostrar: bool = True) -> plt.Figure:
        """
        Cria gráfico de linhas do desvio padrão de renda por região.
        
        Args:
            mostrar: Se True, exibe o gráfico imediatamente
            
        Returns:
            Objeto Figure do matplotlib
        """
        desvio_renda = (
            self.dados
            .groupby('Regiao')['renda_per_capita']
            .std()
            .sort_values(ascending=False)
        )
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(desvio_renda.index, desvio_renda.values, 
               marker='o', linestyle='-', color='teal', 
               linewidth=2, markersize=10, markerfacecolor='coral')
        
        # Área sob a curva
        ax.fill_between(desvio_renda.index, desvio_renda.values, 
                        alpha=0.3, color='teal')
        
        ax.set_title('Variação (Desvio Padrão) da Renda por Região', fontweight='bold')
        ax.set_xlabel('Região')
        ax.set_ylabel('Desvio Padrão (R$)')
        ax.grid(True, linestyle='--', alpha=0.6)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if mostrar:
            plt.show()
        
        return fig
    
    def boxplot_renda_tipo(self, com_outliers: bool = True, 
                           zoom: bool = False, mostrar: bool = True) -> plt.Figure:
        """
        Cria boxplot da distribuição de renda por tipo (Capital vs Interior).
        
        Args:
            com_outliers: Se True, inclui outliers no gráfico
            zoom: Se True, aplica zoom limitando o eixo Y
            mostrar: Se True, exibe o gráfico imediatamente
            
        Returns:
            Objeto Figure do matplotlib
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Preparar dados para boxplot
        tipos = self.dados['Tipo'].unique()
        dados_boxplot = [
            self.dados[self.dados['Tipo'] == tipo]['renda_per_capita'].values 
            for tipo in tipos
        ]
        
        bp = ax.boxplot(dados_boxplot, labels=tipos, showfliers=com_outliers,
                       patch_artist=True, notch=True)
        
        # Colorir as caixas
        colors = ['#66c2a5', '#fc8d62']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        if zoom:
            ax.set_ylim(0, Config.LIMITE_RENDA_ZOOM)
            titulo = 'Distribuição de Renda: Capital vs Interior (Zoom)'
        else:
            titulo = 'Distribuição de Renda: Capital vs Interior'
            if not com_outliers:
                titulo += ' (Sem Outliers)'
        
        ax.set_title(titulo, fontweight='bold')
        ax.set_ylabel('Renda Per Capita (R$)')
        ax.set_xlabel('Tipo de Localidade')
        ax.grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if mostrar:
            plt.show()
        
        return fig
    
    def boxplot_renda_regiao(self, mostrar: bool = True) -> plt.Figure:
        """
        Cria boxplot da distribuição de renda por região.
        
        Args:
            mostrar: Se True, exibe o gráfico imediatamente
            
        Returns:
            Objeto Figure do matplotlib
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        regioes = self.dados.groupby('Regiao')['renda_per_capita'].median().sort_values().index
        dados_boxplot = [
            self.dados[self.dados['Regiao'] == regiao]['renda_per_capita'].values 
            for regiao in regioes
        ]
        
        bp = ax.boxplot(dados_boxplot, labels=regioes, showfliers=False,
                       patch_artist=True, notch=True)
        
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(regioes)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_title('Distribuição de Renda por Região', fontweight='bold')
        ax.set_ylabel('Renda Per Capita (R$)')
        ax.set_xlabel('Região')
        ax.grid(True, axis='y', alpha=0.3)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if mostrar:
            plt.show()
        
        return fig
    
    def histograma_renda(self, bins: int = 30, mostrar: bool = True) -> plt.Figure:
        """
        Cria histograma da distribuição de renda.
        
        Args:
            bins: Número de bins do histograma
            mostrar: Se True, exibe o gráfico imediatamente
            
        Returns:
            Objeto Figure do matplotlib
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.hist(self.dados['renda_per_capita'], bins=bins, 
               color='steelblue', edgecolor='white', alpha=0.7)
        
        # Linha vertical para a média e mediana
        media = self.dados['renda_per_capita'].mean()
        mediana = self.dados['renda_per_capita'].median()
        
        ax.axvline(media, color='red', linestyle='--', linewidth=2, 
                  label=f'Média: R$ {media:.0f}')
        ax.axvline(mediana, color='green', linestyle='-', linewidth=2, 
                  label=f'Mediana: R$ {mediana:.0f}')
        
        ax.set_title('Distribuição da Renda Per Capita', fontweight='bold')
        ax.set_xlabel('Renda Per Capita (R$)')
        ax.set_ylabel('Frequência')
        ax.legend()
        
        plt.tight_layout()
        
        if mostrar:
            plt.show()
        
        return fig
    
    def dashboard_completo(self) -> None:
        """
        Gera um dashboard com múltiplas visualizações em uma única figura.
        """
        fig = plt.figure(figsize=(16, 12))
        
        # Grid de subplots
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.25)
        
        # 1. Histograma de renda
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.hist(self.dados['renda_per_capita'], bins=30, 
                color='steelblue', edgecolor='white', alpha=0.7)
        ax1.axvline(self.dados['renda_per_capita'].mean(), color='red', 
                   linestyle='--', linewidth=2, label='Média')
        ax1.set_title('Distribuição da Renda Per Capita', fontweight='bold')
        ax1.set_xlabel('Renda (R$)')
        ax1.legend()
        
        # 2. Barras por região
        ax2 = fig.add_subplot(gs[0, 1])
        media_regiao = self.dados.groupby('Regiao')['renda_per_capita'].mean().sort_values()
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(media_regiao)))
        ax2.barh(range(len(media_regiao)), media_regiao.values, color=colors)
        ax2.set_yticks(range(len(media_regiao)))
        ax2.set_yticklabels(media_regiao.index, fontsize=8)
        ax2.set_title('Renda Média por Região', fontweight='bold')
        ax2.set_xlabel('Renda (R$)')
        
        # 3. Boxplot Capital vs Interior
        ax3 = fig.add_subplot(gs[1, 0])
        tipos = ['Capital', 'Interior']
        dados_box = [self.dados[self.dados['Tipo'] == t]['renda_per_capita'] for t in tipos]
        bp = ax3.boxplot(dados_box, labels=tipos, patch_artist=True, showfliers=False)
        bp['boxes'][0].set_facecolor('#66c2a5')
        bp['boxes'][1].set_facecolor('#fc8d62')
        ax3.set_title('Renda: Capital vs Interior', fontweight='bold')
        ax3.set_ylabel('Renda (R$)')
        
        # 4. Contagem por faixa de renda
        ax4 = fig.add_subplot(gs[1, 1])
        faixa_counts = self.dados['Faixa_Renda'].value_counts()
        colors = ['#d73027', '#fc8d59', '#fee08b', '#91cf60', '#1a9850']
        ax4.pie(faixa_counts.values, labels=faixa_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax4.set_title('Distribuição por Faixa de Renda', fontweight='bold')
        
        # 5. Top 10 Estados
        ax5 = fig.add_subplot(gs[2, :])
        media_uf = self.dados.groupby('UF')['renda_per_capita'].mean().sort_values(ascending=False).head(15)
        colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(media_uf)))
        ax5.bar(media_uf.index.astype(str), media_uf.values, color=colors)
        ax5.axhline(y=self.dados['renda_per_capita'].mean(), color='red', 
                   linestyle='--', linewidth=2, label='Média Geral')
        ax5.set_title('Top 15 Estados por Renda Média', fontweight='bold')
        ax5.set_xlabel('Estado (UF)')
        ax5.set_ylabel('Renda (R$)')
        ax5.legend()
        plt.xticks(rotation=45)
        
        plt.suptitle('Dashboard de Análise de Renda Per Capita', 
                    fontsize=16, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        plt.show()
    
    def executar_todas_visualizacoes(self) -> None:
        """Executa todas as visualizações em sequência."""
        logger.info("\n" + "="*60)
        logger.info("GERANDO VISUALIZAÇÕES")
        logger.info("="*60 + "\n")
        
        visualizacoes = [
            ("Gráfico de Barras - Renda por Região", self.grafico_barras_renda_regiao),
            ("Gráfico de Pizza - Distribuição por Região", self.grafico_pizza_distribuicao),
            ("Gráfico de Barras - Renda por Estado", self.grafico_barras_renda_estado),
            ("Gráfico de Linhas - Desvio Padrão", self.grafico_linha_desvio_renda),
            ("Boxplot - Capital vs Interior", lambda: self.boxplot_renda_tipo(com_outliers=True)),
            ("Boxplot - Capital vs Interior (Sem Outliers)", lambda: self.boxplot_renda_tipo(com_outliers=False)),
            ("Boxplot - Capital vs Interior (Zoom)", lambda: self.boxplot_renda_tipo(zoom=True)),
            ("Histograma - Distribuição de Renda", self.histograma_renda),
            ("Boxplot - Por Região", self.boxplot_renda_regiao),
        ]
        
        for nome, func in visualizacoes:
            logger.info(f"Gerando: {nome}")
            func()


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal que orquestra todo o pipeline."""
    
    logger.info("\n" + "="*60)
    logger.info("ANÁLISE DE DADOS - CEP E RENDA PER CAPITA")
    logger.info("="*60 + "\n")
    
    # 1. Engenharia de Dados
    engenharia = EngenhariaDados(Config.ARQUIVO_DADOS)
    engenharia.processar_pipeline()
    
    # Análise de variação
    engenharia.analisar_variacao_renda()
    
    # Obter dados processados
    dados = engenharia.obter_dados()
    
    if dados is None:
        logger.error("Não foi possível processar os dados. Encerrando.")
        return
    
    # 2. Visualização de Dados
    visualizacao = VisualizacaoDados(dados)
    
    # Opção 1: Dashboard completo (uma única figura com vários gráficos)
    # visualizacao.dashboard_completo()
    
    # Opção 2: Visualizações individuais
    visualizacao.executar_todas_visualizacoes()
    
    logger.info("\n" + "="*60)
    logger.info("ANÁLISE CONCLUÍDA COM SUCESSO!")
    logger.info("="*60)


if __name__ == "__main__":
    main()
