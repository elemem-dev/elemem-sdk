#!/bin/bash

# GitHub Release 大文件上传脚本
# 支持上传超过 1GB 的文件到 GitHub Release

set -x

# 配置变量
GITHUB_TOKEN=""
REPO_OWNER="elemem-dev"
REPO_NAME="elemem-sdk"
TAG_NAME="v2.0.1.0"
RELEASE_NAME="Release v2.0.1.0"
RELEASE_BODY="This release contains large files"
FILE_PATH="release/elemem-vector.tar"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查文件大小
check_file_size() {
    local file="$1"
    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    local size_gb=$(echo "scale=2; $size / 1024 / 1024 / 1024" | bc)
    
    echo "File size: ${size_gb} GB"
    
    if (( $(echo "$size > 2147483648" | bc -l) )); then
        echo -e "${RED}Warning: File is larger than 2GB. GitHub Release limit is 2GB per file.${NC}"
        return 1
    fi
    return 0
}

# 创建 Release
create_release() {
    response=$(curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
                   -H "Content-Type: application/json" \
                   "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/releases" \
                   -d @- << EOF
{
    "tag_name": "$TAG_NAME",
    "name": "$RELEASE_NAME",
    "body": "$RELEASE_BODY",
    "draft": false,
    "prerelease": false
}
EOF
)

    upload_url=$(echo "$response" | grep -o '"upload_url": "[^"]*' | cut -d'"' -f4 | sed 's/{[^}]*}//')

    if [ -z "$upload_url" ]; then
        echo -e "${RED}Failed to create release${NC}" >&2
        echo "$response" >&2
        return 1
    else
        echo "$upload_url"
        return 0
    fi
}

# 上传大文件
upload_large_file() {
    local upload_url="$1"
    local file_path="$2"
    local file_name=$(basename "$file_path")
    
    echo "Uploading $file_name..."
    
    # 使用 curl 上传大文件
    curl -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Content-Type: application/octet-stream" \
        --data-binary @"$file_path" \
        --progress-bar \
        "${upload_url}?name=${file_name}" \
        -o upload_response.json
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}File uploaded successfully${NC}"
        return 0
    else
        echo -e "${RED}Failed to upload file${NC}"
        return 1
    fi
}

# 主函数
main() {
    echo "GitHub Large File Release Uploader"
    echo "=================================="
    
    # 检查文件是否存在
    if [ ! -f "$FILE_PATH" ]; then
        echo -e "${RED}Error: File not found: $FILE_PATH${NC}"
        exit 1
    fi
    
    # 检查文件大小
    if ! check_file_size "$FILE_PATH"; then
        echo "Consider splitting the file into parts smaller than 2GB"
        exit 1
    fi
    
    # 创建 Release
    UPLOAD_URL=$(create_release)
    if [ $? -ne 0 ] || [ -z "$UPLOAD_URL" ]; then
        echo -e "${RED}Release creation failed!${NC}"
        exit 1
    fi

    echo "Release created successfully:"
    echo "$UPLOAD_URL"
    
    # 上传文件
    upload_large_file "$UPLOAD_URL" "$FILE_PATH"
}

# 执行主函数
main