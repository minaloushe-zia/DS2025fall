#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最大子数组和问题 - 三种算法实现与性能对比
Maximum Subarray Sum Problem - Three Algorithm Implementations and Performance Comparison

包含算法 (Algorithms Included):
1. 暴力枚举 (Brute Force Enumeration)
2. 优化枚举 (Optimized Enumeration) 
3. 动态规划 (Dynamic Programming - Kadane's Algorithm)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import time
import random
from tqdm import tqdm
import platform
from typing import List, Tuple, Dict, Any
import warnings
import os
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.font_manager._rebuild()
except:
    pass

# 方法1：设置全局字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "WenQuanYi Micro Hei", "Heiti TC", "DejaVu Sans"]
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

class FontManager:
    
    def __init__(self):
        self._configure_matplotlib()
    
    def _configure_matplotlib(self):
        """配置matplotlib字体设置 (Configure matplotlib font settings)"""
        # 设置seaborn样式（这可能会重置字体）
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        
        # 在seaborn设置之后重新设置字体
        plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "WenQuanYi Micro Hei", "Heiti TC", "DejaVu Sans"]
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 10
        

class MaxSubarrayAlgorithms:
    """最大子数组和算法集合 (Maximum Subarray Sum Algorithms Collection)"""
    
    def __init__(self):
        self.font_manager = FontManager()
        self.results = {}
    
    def brute_force(self, arr: List[int], show_progress: bool = True) -> Tuple[int, int, int]:
        """
        暴力枚举算法 (Brute Force Algorithm)
        时间复杂度: O(n³) (Time Complexity: O(n³))
        空间复杂度: O(1) (Space Complexity: O(1))
        """
        n = len(arr)
        max_sum = float('-inf')
        start_idx = 0
        end_idx = 0
        
        # 计算总的迭代次数
        total_iterations = n * (n + 1) // 2
        
        if show_progress:
            pbar = tqdm(total=total_iterations, 
                       desc="暴力枚举 (Brute Force)", 
                       unit="iter",
                       ncols=80)
        
        iteration_count = 0
        
        # 枚举所有可能的子数组
        for i in range(n):
            for j in range(i, n):
                # 计算子数组 arr[i:j+1] 的和
                current_sum = 0
                for k in range(i, j + 1):
                    current_sum += arr[k]
                
                # 更新最大值
                if current_sum > max_sum:
                    max_sum = current_sum
                    start_idx = i
                    end_idx = j
                
                iteration_count += 1
                if show_progress:
                    pbar.update(1)
        
        if show_progress:
            pbar.close()
        
        return max_sum, start_idx, end_idx
    
    def optimized_enumeration(self, arr: List[int], show_progress: bool = True) -> Tuple[int, int, int]:
        """
        优化枚举算法 (Optimized Enumeration Algorithm)
        时间复杂度: O(n²) (Time Complexity: O(n²))
        空间复杂度: O(1) (Space Complexity: O(1))
        """
        n = len(arr)
        max_sum = float('-inf')
        start_idx = 0
        end_idx = 0
        
        # 计算总的迭代次数
        total_iterations = n * (n + 1) // 2
        
        if show_progress:
            pbar = tqdm(total=total_iterations, 
                       desc="优化枚举 (Optimized Enum)", 
                       unit="iter",
                       ncols=80)
        
        iteration_count = 0
        
        # 枚举所有可能的起始位置
        for i in range(n):
            current_sum = 0
            # 从起始位置开始累加
            for j in range(i, n):
                current_sum += arr[j]
                
                # 更新最大值
                if current_sum > max_sum:
                    max_sum = current_sum
                    start_idx = i
                    end_idx = j
                
                iteration_count += 1
                if show_progress:
                    pbar.update(1)
        
        if show_progress:
            pbar.close()
        
        return max_sum, start_idx, end_idx
    
    def dynamic_programming(self, arr: List[int], show_progress: bool = True) -> Tuple[int, int, int]:
        """
        动态规划算法 - Kadane算法 (Dynamic Programming - Kadane's Algorithm)
        时间复杂度: O(n) (Time Complexity: O(n))
        空间复杂度: O(1) (Space Complexity: O(1))
        """
        n = len(arr)
        max_sum = float('-inf')
        current_sum = 0
        start_idx = 0
        end_idx = 0
        temp_start = 0
        
        if show_progress:
            pbar = tqdm(total=n, 
                       desc="动态规划 (Dynamic Programming)", 
                       unit="iter",
                       ncols=80)
        
        for i in range(n):
            current_sum += arr[i]
            
            # 如果当前和大于最大和，更新最大和和结束位置
            if current_sum > max_sum:
                max_sum = current_sum
                start_idx = temp_start
                end_idx = i
            
            # 如果当前和小于0，重置当前和和临时起始位置
            if current_sum < 0:
                current_sum = 0
                temp_start = i + 1
            
            if show_progress:
                pbar.update(1)
        
        if show_progress:
            pbar.close()
        
        return max_sum, start_idx, end_idx
    
    def compare_algorithms(self, test_sizes: List[int] = None) -> Dict[str, Any]:
        """
        算法性能对比 (Algorithm Performance Comparison)
        """
        if test_sizes is None:
            test_sizes = [10, 50, 100, 200, 500, 1000]
        
        results = {
            'sizes': test_sizes,
            'brute_force_times': [],
            'optimized_enum_times': [],
            'dynamic_prog_times': [],
            'algorithms': ['暴力枚举\n(Brute Force)', '优化枚举\n(Optimized Enum)', '动态规划\n(Dynamic Programming)'],
            'complexities': ['O(n³)', 'O(n²)', 'O(n)']
        }
        
        print("\n" + "="*60)
        print("算法性能对比测试 (Algorithm Performance Comparison Test)")
        print("="*60)
        
        for size in test_sizes:
            print(f"\n测试数组大小 (Testing Array Size): {size}")
            
            # 生成随机测试数据
            test_array = [random.randint(-100, 100) for _ in range(size)]
            
            # 测试暴力枚举算法
            if size <= 500:  # 对于大数组，跳过暴力枚举以节省时间
                start_time = time.time()
                max_sum1, start1, end1 = self.brute_force(test_array, show_progress=False)
                brute_force_time = time.time() - start_time
                results['brute_force_times'].append(brute_force_time)
                print(f"  暴力枚举 (Brute Force): {brute_force_time:.4f}s")
            else:
                results['brute_force_times'].append(None)
                print(f"  暴力枚举 (Brute Force): 跳过 (Skipped) - 数组过大")
            
            # 测试优化枚举算法
            start_time = time.time()
            max_sum2, start2, end2 = self.optimized_enumeration(test_array, show_progress=False)
            optimized_enum_time = time.time() - start_time
            results['optimized_enum_times'].append(optimized_enum_time)
            print(f"  优化枚举 (Optimized Enum): {optimized_enum_time:.4f}s")
            
            # 测试动态规划算法
            start_time = time.time()
            max_sum3, start3, end3 = self.dynamic_programming(test_array, show_progress=False)
            dynamic_prog_time = time.time() - start_time
            results['dynamic_prog_times'].append(dynamic_prog_time)
            print(f"  动态规划 (Dynamic Programming): {dynamic_prog_time:.4f}s")
            
            # 验证结果一致性
            if size <= 500:
                if max_sum1 == max_sum2 == max_sum3:
                    print(f"  ✓ 结果验证通过 (Results Verified): 最大和 = {max_sum1}")
                else:
                    print(f"  ✗ 结果不一致 (Results Inconsistent)!")
            else:
                if max_sum2 == max_sum3:
                    print(f"  ✓ 结果验证通过 (Results Verified): 最大和 = {max_sum2}")
                else:
                    print(f"  ✗ 结果不一致 (Results Inconsistent)!")
        
        self.results = results
        return results
    
    def visualize_performance(self, save_path: str = None):
        """
        可视化算法性能对比 (Visualize Algorithm Performance Comparison)
        逐张绘制和保存图表 (Draw and save charts one by one)
        """
        if not self.results:
            print("请先运行 compare_algorithms() 方法 (Please run compare_algorithms() first)")
            return
        
        sizes = self.results['sizes']
        base_path = save_path or 'e:\\2025fall\\DS'
        
        # 图表列表用于进度条
        charts = [
            "时间复杂度理论对比图 (Theoretical Time Complexity)",
            "算法复杂度总结表 (Algorithm Complexity Summary)"
        ]
        
        print("\n开始绘制算法性能对比图表...")
        print("Starting to draw algorithm performance comparison charts...")
        
        # 使用进度条显示绘图进度
        for i, chart_name in enumerate(tqdm(charts, desc="绘制图表 (Drawing Charts)", 
                                          bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')):
            
            # 创建单独的图形
            plt.figure(figsize=(12, 8))
            
            if i == 0:  # 时间复杂度理论对比图
                plt.title('时间复杂度理论对比\nTheoretical Time Complexity Comparison', 
                         fontsize=16, fontweight='bold', pad=20)
                
                n_values = np.array(sizes)
                # 使用更高级的颜色配置
                plt.plot(n_values, n_values**3 / 1e6, color='#E74C3C', linestyle='--', 
                        label='O(n³) - 暴力枚举 (Brute Force)', linewidth=3.5, alpha=0.9)
                plt.plot(n_values, n_values**2 / 1e4, color='#27AE60', linestyle='--', 
                        label='O(n²) - 优化枚举 (Optimized Enum)', linewidth=3.5, alpha=0.9)
                plt.plot(n_values, n_values / 10, color='#3498DB', linestyle='--', 
                        label='O(n) - 动态规划 (Dynamic Programming)', linewidth=3.5, alpha=0.9)
                
                plt.xlabel('数组大小 (Array Size)', fontsize=14)
                plt.ylabel('相对时间单位 (Relative Time Units)', fontsize=14)
                plt.legend(fontsize=12)
                plt.grid(True, alpha=0.3)
                plt.yscale('log')
                
                save_file = os.path.join(base_path, '图2_时间复杂度理论对比_Theoretical_Complexity.png')
                
            elif i == 1:  # 算法复杂度总结表
                plt.figure(figsize=(14, 8))
                plt.axis('tight')
                plt.axis('off')
                plt.title('算法复杂度总结\nAlgorithm Complexity Summary', 
                         fontsize=18, fontweight='bold', pad=30)
                
                table_data = [
                    ['算法名称\nAlgorithm', '时间复杂度\nTime Complexity', 
                     '空间复杂度\nSpace Complexity', '适用场景\nUse Case', '特点\nCharacteristics'],
                    ['暴力枚举\nBrute Force', 'O(n³)', 'O(1)', '小数组\nSmall Arrays', 
                     '简单直观\nSimple & Intuitive'],
                    ['优化枚举\nOptimized Enum', 'O(n²)', 'O(1)', '中等数组\nMedium Arrays', 
                     '空间优化\nSpace Optimized'],
                    ['动态规划\nDynamic Programming', 'O(n)', 'O(1)', '所有大小\nAll Sizes', 
                     '最优解法\nOptimal Solution']
                ]
                
                table = plt.table(cellText=table_data[1:], colLabels=table_data[0], 
                                 cellLoc='center', loc='center',
                                 colWidths=[0.25, 0.2, 0.2, 0.2, 0.25])
                table.auto_set_font_size(False)
                table.set_fontsize(12)
                table.scale(1, 3)
                
                # 设置表格样式 - 使用更高级的颜色配置
                for i in range(len(table_data)):
                    for j in range(len(table_data[0])):
                        cell = table[(i, j)]
                        if i == 0:  # 表头
                            cell.set_facecolor('#2C3E50')  # 深蓝灰色
                            cell.set_text_props(weight='bold', color='white')
                        else:
                            if i % 2 == 1:
                                cell.set_facecolor('#ECF0F1')  # 浅灰色
                            else:
                                cell.set_facecolor('#D5DBDB')  # 中灰色
                            cell.set_edgecolor('#BDC3C7')  # 边框颜色
                            cell.set_linewidth(1.5)
                
                save_file = os.path.join(base_path, '图4_算法复杂度总结表_Complexity_Summary.png')
                

            
            # 保存当前图表
            plt.tight_layout()
            plt.savefig(save_file, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"✓ 已保存: {os.path.basename(save_file)}")
            print(f"  Saved: {os.path.basename(save_file)}")
            
            # 显示图表
            plt.show()
            plt.close()  # 关闭当前图形以释放内存
        
        print(f"\n所有图表已保存到目录: {base_path}")
        print(f"All charts have been saved to directory: {base_path}")
        print("=" * 60)

def main():
    """主函数 (Main Function)"""
    print("="*80)
    print("最大子数组和问题 - 三种算法实现与性能对比")
    print("Maximum Subarray Sum Problem - Three Algorithm Implementations and Performance Comparison")
    print("="*80)
    
    # 创建算法实例
    algorithms = MaxSubarrayAlgorithms()
    
    # 示例数组
    example_array = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"\n示例数组 (Example Array): {example_array}")
    print(f"数组长度 (Array Length): {len(example_array)}")
    
    print("\n" + "-"*60)
    print("算法演示 (Algorithm Demonstration)")
    print("-"*60)
    
    # 1. 暴力枚举算法演示
    print("\n1. 暴力枚举算法 (Brute Force Algorithm)")
    print("   时间复杂度 (Time Complexity): O(n³)")
    max_sum1, start1, end1 = algorithms.brute_force(example_array)
    print(f"   结果 (Result): 最大和 = {max_sum1}, 子数组位置 = [{start1}:{end1+1}]")
    print(f"   子数组 (Subarray): {example_array[start1:end1+1]}")
    
    # 2. 优化枚举算法演示
    print("\n2. 优化枚举算法 (Optimized Enumeration Algorithm)")
    print("   时间复杂度 (Time Complexity): O(n²)")
    max_sum2, start2, end2 = algorithms.optimized_enumeration(example_array)
    print(f"   结果 (Result): 最大和 = {max_sum2}, 子数组位置 = [{start2}:{end2+1}]")
    print(f"   子数组 (Subarray): {example_array[start2:end2+1]}")
    
    # 3. 动态规划算法演示
    print("\n3. 动态规划算法 (Dynamic Programming Algorithm)")
    print("   时间复杂度 (Time Complexity): O(n)")
    max_sum3, start3, end3 = algorithms.dynamic_programming(example_array)
    print(f"   结果 (Result): 最大和 = {max_sum3}, 子数组位置 = [{start3}:{end3+1}]")
    print(f"   子数组 (Subarray): {example_array[start3:end3+1]}")
    
    # 验证结果一致性
    if max_sum1 == max_sum2 == max_sum3:
        print(f"\n✓ 所有算法结果一致 (All algorithms produce consistent results)")
    else:
        print(f"\n✗ 算法结果不一致 (Algorithms produce inconsistent results)")
    
    # 性能对比测试
    print("\n" + "-"*60)
    print("性能对比测试 (Performance Comparison Test)")
    print("-"*60)
    
    test_sizes = [10, 50, 100, 200, 500, 1000]
    results = algorithms.compare_algorithms(test_sizes)
    
    # 生成可视化图表
    print("\n" + "-"*60)
    print("生成可视化图表 (Generating Visualization Charts)")
    print("-"*60)
    
    algorithms.visualize_performance()
    
    print("\n" + "="*80)
    print("程序执行完成 (Program Execution Completed)")
    print("="*80)

if __name__ == "__main__":
    main()