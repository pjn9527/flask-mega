#!/bin/bash
# 自动上传 GitHub 脚本（含变更检查）

echo "🔍 检查文件改动情况..."
git status

echo ""
read -p "是否继续提交并推送到 GitHub？(y/n): " confirm
if [ "$confirm" != "y" ]; then
  echo "🚫 已取消操作。"
  exit 1
fi

read -p "请输入提交备注: " msg
git add .
git commit -m "$msg"
git push origin main
