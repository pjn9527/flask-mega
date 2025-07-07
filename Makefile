.PHONY: push

# 调用push_with_status的shell脚本的bash快捷指令
push:
	@bash push_with_status.sh

# 检查容器状态，需在服务器终端执行
container-status:
	@docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
