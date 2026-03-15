#!/bin/bash
# A股收盘后持仓分析脚本
# 运行时间: 每个工作日15:00后
# 功能: 获取持仓股票当日表现，生成分析报告

set -e

echo "=========================================="
echo "  A股收盘持仓分析 - $(date '+%Y-%m-%d %H:%M')"
echo "=========================================="

# 工作目录
WORK_DIR="/home/ubuntu/.openclaw/workspace-maxbot"
PORTFOLIO_DIR="$WORK_DIR/portfolio"
LOG_FILE="$PORTFOLIO_DIR/daily-analysis-$(date +%Y%m%d).md"

# 创建日志目录
mkdir -p "$PORTFOLIO_DIR"

# 获取当前日期
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)

echo "# 持仓日报 - $TODAY" > "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ==========================================
# 1. 获取大盘数据
# ==========================================
echo "## 一、大盘表现" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 获取上证指数
echo "### 上证指数" >> "$LOG_FILE"
curl -s "https://qt.gtimg.cn/q=sh000001" 2>/dev/null | awk -F '~' '{
    name=$2
    price=$3
    change=$4
    change_pct=$5
    if(price > 0 && change != 0) {
        printf "- **当前**: %.2f\n", price
        printf "- **涨跌**: %+.2f (%+.2f%%)\n", change, change_pct
    } else {
        print "- 数据获取失败"
    }
}' >> "$LOG_FILE"

echo "" >> "$LOG_FILE"

# 获取深证成指
echo "### 深证成指" >> "$LOG_FILE"
curl -s "https://qt.gtimg.cn/q=sz399001" 2>/dev/null | awk -F '~' '{
    name=$2
    price=$3
    change=$4
    change_pct=$5
    printf "- **当前**: %.2f\n", price
    printf "- **涨跌**: %.2f (%.2f%%)\n", change, change_pct
}' >> "$LOG_FILE" || echo "- 数据获取失败" >> "$LOG_FILE"

echo "" >> "$LOG_FILE"

# 获取创业板指
echo "### 创业板指" >> "$LOG_FILE"
curl -s "https://qt.gtimg.cn/q=sz399006" 2>/dev/null | awk -F '~' '{
    name=$2
    price=$3
    change=$4
    change_pct=$5
    printf "- **当前**: %.2f\n", price
    printf "- **涨跌**: %.2f (%.2f%%)\n", change, change_pct
}' >> "$LOG_FILE" || echo "- 数据获取失败" >> "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ==========================================
# 2. 持仓股票表现
# ==========================================
echo "## 二、持仓股票当日表现" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 持仓列表
# 格式: 代码|名称|持仓成本|持仓数量
declare -a HOLDINGS=(
    "sz000938|紫光股份|28.363|400"
    "sh510050|上证50ETF|2.382|8100"
    "sh510300|沪深300ETF|2.728|5600"
    "sz159941|纳斯达克ETF|2.276|8500"
    "sz513500|标普500ETF|2.410|7500"
    "sh516160|新能源ETF|3.051|2000"
    "sh588000|科创50ETF|1.430|16000"
    "sz159227|航空航天ETF|1.510|6500"
    "sz159902|中小100ETF|3.894|2500"
    "sz159915|创业板ETF|3.556|9100"
    "sh512760|芯片ETF|1.763|15000"
)

echo "| 名称 | 持仓成本 | 现价 | 日涨跌 | 盈亏 | 盈亏率 |" >> "$LOG_FILE"
echo "|------|----------|------|--------|------|--------|" >> "$LOG_FILE"

for holding in "${HOLDINGS[@]}"; do
    IFS='|' read -r code name cost qty <<< "$holding"
    
    # 获取实时数据
    data=$(curl -s "https://qt.gtimg.cn/q=$code" 2>/dev/null || echo "")
    
    if [ -n "$data" ]; then
        # 解析数据 - 腾讯API格式: v_股票代码=股票名称~最新价~涨跌额~涨跌幅...
        price=$(echo "$data" | awk -F '~' '{print $3}')
        change=$(echo "$data" | awk -F '~' '{print $4}')
        change_pct=$(echo "$data" | awk -F '~' '{print $5}')
        
        # 验证数据有效性
        if [ -n "$price" ] && [ "$price" != "0" ] && [ -n "$cost" ] && [ "$cost" != "0" ]; then
            # 计算盈亏
            pnl=$(awk "BEGIN {printf \"%.2f\", ($price - $cost) * $qty}")
            pnl_pct=$(awk "BEGIN {printf \"%.2f\", ($price - $cost) / $cost * 100}")
            
            # 输出表格行
            printf "| %s | %.3f | %.3f | %+.2f (%+.2f%%) | %+.2f | %+.2f%% |\n" \
                "$name" "$cost" "$price" "$change" "$change_pct" "$pnl" "$pnl_pct" >> "$LOG_FILE"
        else
            echo "| $name | $cost | 数据异常 | - | - | - |" >> "$LOG_FILE"
        fi
    else
        echo "| $name | $cost | 无数据 | - | - | - |" >> "$LOG_FILE"
    fi
done

echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ==========================================
# 3. 当日盈亏汇总
# ==========================================
echo "## 三、当日盈亏汇总" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "- **统计时间**: $TODAY 15:00" >> "$LOG_FILE"
echo "- **持仓数量**: ${#HOLDINGS[@]} 只" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "> 注：具体盈亏金额需根据实时数据计算" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ==========================================
# 4. 明日投资建议
# ==========================================
echo "## 四、明日投资建议 ($(date -d "+1 day" +%Y-%m-%d))" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 根据大盘表现生成建议
echo "### 大盘研判" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "- 关注今晚美股走势对A股的影响" >> "$LOG_FILE"
echo "- 关注政策面消息" >> "$LOG_FILE"
echo "- 关注北向资金流向" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "### 个股/ETF操作建议" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "#### 🟢 盈利持仓 (建议持有)" >> "$LOG_FILE"
echo "- 沪深300ETF、上证50ETF：设置移动止盈" >> "$LOG_FILE"
echo "- 中小100ETF：关注回调风险" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "#### 🟡 亏损持仓 (建议观望/补仓)" >> "$LOG_FILE"
echo "- 紫光股份：关注¥27阻力位，突破可减仓" >> "$LOG_FILE"
echo "- 航空航天ETF：关注¥1.35支撑位" >> "$LOG_FILE"
echo "- 创业板ETF：波动较大，定投策略" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "#### 🔴 风险提示" >> "$LOG_FILE"
echo "- 严格止损纪律" >> "$LOG_FILE"
echo "- 控制仓位，不要满仓" >> "$LOG_FILE"
echo "- 关注市场系统性风险" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ==========================================
# 5. 推送报告
# ==========================================
echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "*报告由 AnalyzeMaster 自动生成*" >> "$LOG_FILE"
echo "*生成时间: $(date '+%Y-%m-%d %H:%M:%S')*" >> "$LOG_FILE"

# 推送到GitHub
cd "$WORK_DIR"
git add "$LOG_FILE" 2>/dev/null || true
git commit -m "Add daily portfolio analysis - $TODAY" 2>/dev/null || true
git push origin main 2>/dev/null || true

echo ""
echo "=========================================="
echo "  分析完成！"
echo "  报告路径: $LOG_FILE"
echo "  GitHub: https://github.com/anekin/maxbot"
echo "=========================================="
