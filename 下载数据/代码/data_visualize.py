import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import mplcursors  # 导入 mplcursors

# 定义文件路径
world_path = r"D:\python课程\data_visualization\下载数据\data\Natural Earth 数据集\ne_110m_admin_0_countries\ne_110m_admin_0_countries.shp"
eq_path = r"D:\python课程\data_visualization\下载数据\data\eq_data\eq_data_7_day_m1.geojson"
fire_path = r"D:\python课程\data_visualization\下载数据\data\eq_data\world_fires_1_day.csv"

def setup_chinese_font():
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    return font

def read_data(world_path, eq_path, fire_path):
    try:
        world = gpd.read_file(world_path)
        gdf_eq = gpd.read_file(eq_path)
        fires = pd.read_csv(fire_path)
        gdf_fires = gpd.GeoDataFrame(fires, geometry=gpd.points_from_xy(fires.longitude, fires.latitude))
        return world, gdf_eq, gdf_fires
    except Exception as e:
        print(f"Error reading data: {e}")

def plot_base_map(ax, world, projection):
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    world.plot(ax=ax, edgecolor='black', facecolor='lightgray')

def plot_data(ax, gdf_eq, gdf_fires, projection):
    scatter_eq = ax.scatter(gdf_eq.geometry.x, gdf_eq.geometry.y, c=gdf_eq['mag'],
                            s=gdf_eq['mag']*10, cmap='Reds', alpha=0.6, edgecolor='black',
                            label='地震', transform=ccrs.PlateCarree())
    scatter_fire = ax.scatter(gdf_fires.geometry.x, gdf_fires.geometry.y, c=gdf_fires['brightness'],
                              s=(gdf_fires['brightness']/20)*2, cmap='viridis', alpha=0.6, edgecolor='black',
                              marker='D', label='火灾', transform=ccrs.PlateCarree())
    return scatter_eq, scatter_fire

def create_map():
    font = setup_chinese_font()
    projection = ccrs.PlateCarree()
    fig = plt.figure(figsize=(12, 7))  #修改界面大小

    # 创建地图的轴--position修改地图大小位置
    ax = fig.add_subplot(1, 2, 1, projection=projection, position=[0.07, 0.04, 0.7, 0.9])
    
    world, gdf_eq, gdf_fires = read_data(world_path, eq_path, fire_path)
    plot_base_map(ax, world, projection)
    
    scatter_eq, scatter_fire = plot_data(ax, gdf_eq, gdf_fires, projection)
    
    # 创建颜色棒的轴
    cax1 = fig.add_axes([0.82, 0.19, 0.02, 0.6])  # [left, bottom, width, height]
    cbar_eq = fig.colorbar(scatter_eq, cax=cax1, orientation='vertical')
    cbar_eq.set_label('震级', rotation=0, fontsize=16, labelpad=20)
    
    cax2 = fig.add_axes([0.90, 0.19, 0.02, 0.6])  # [left, bottom, width, height]
    cbar_fire = fig.colorbar(scatter_fire, cax=cax2, orientation='vertical')
    cbar_fire.set_label('火级', rotation=0, fontsize=16, labelpad=20)
    
    # 使用 ax.text 添加标题和坐标轴标签
    ax.text(0.5, 1.20, '全球地震和火灾散点图', fontsize=30, fontproperties=font, ha='center', transform=ax.transAxes)
    ax.text(0.5, -0.15, '经度', fontsize=16, fontproperties=font, ha='center', transform=ax.transAxes)
    ax.text(-0.09, 0.5, '纬度', fontsize=16, fontproperties=font, va='center', rotation='vertical', transform=ax.transAxes)
    
    # 添加 mplcursors 到散点图
    cursor_eq = mplcursors.cursor(scatter_eq, hover=True)
    @cursor_eq.connect("add")
    def on_add(sel):
        # 显示地震的震级
        if sel.target is not None and len(sel.target) > 0:
            x, y = sel.target[:2]
            mag = gdf_eq.iloc[sel.index]['mag']
            sel.annotation.set_text(f"经度: {x:.2f}, 纬度: {y:.2f}, 震级: {mag:.2f}")
            sel.annotation.get_bbox_patch().set(alpha=0.8)
    
    cursor_fire = mplcursors.cursor(scatter_fire, hover=True)
    @cursor_fire.connect("add")
    def on_add(sel):
        # 显示火灾的火级
        if sel.target is not None and len(sel.target) > 0:
            x, y = sel.target[:2]
            brightness = gdf_fires.iloc[sel.index]['brightness']
            sel.annotation.set_text(f"经度: {x:.2f}, 纬度: {y:.2f}, 火级: {brightness:.2f}")
            sel.annotation.get_bbox_patch().set(alpha=0.8)
    
    ax.gridlines(draw_labels=True, dms=False, x_inline=False, y_inline=False)
    ax.legend(loc='upper right', fontsize=10)
    plt.show()

# 调用函数创建地图
create_map()