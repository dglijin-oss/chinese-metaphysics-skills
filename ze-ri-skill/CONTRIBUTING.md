# 贡献指南

感谢你对本技能的关注！欢迎贡献代码、报告问题或提出建议。

## 🤝 如何贡献

### 1. 报告问题 (Issues)

发现 Bug 或有功能建议？请创建 Issue：

- **Bug 报告**：请提供复现步骤、预期结果、实际结果
- **功能建议**：请说明使用场景、期望功能
- **问题咨询**：请详细描述你的问题

### 2. 提交代码 (Pull Requests)

欢迎提交 PR！请遵循以下流程：

```bash
# 1. Fork 仓库
git clone https://github.com/dglijin-oss/[skill-name].git

# 2. 创建分支
git checkout -b feature/your-feature-name

# 3. 进行修改
# ... 编辑代码 ...

# 4. 运行测试
python3 tests/test_*.py

# 5. 提交更改
git add .
git commit -m "feat: 添加 XXX 功能"

# 6. 推送到远程
git push origin feature/your-feature-name

# 7. 创建 Pull Request
```

### 3. 代码规范

#### Python 代码

```python
# 使用 4 个空格缩进
def function_name(param1, param2):
    """函数文档字符串"""
    # 注释说明
    return result

# 类型注解
def calculate(a: int, b: int) -> int:
    return a + b
```

#### JavaScript 代码

```javascript
/**
 * 函数文档字符串
 * @param {string} param - 参数说明
 * @returns {string} 返回值说明
 */
function functionName(param) {
    // 注释说明
    return result;
}
```

### 4. 提交信息规范

遵循 [约定式提交](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` 修复 Bug
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构（既非新功能也非 Bug 修复）
- `test:` 添加或修改测试
- `chore:` 构建过程或辅助工具变动

示例：
```
feat: 添加流年推算功能
fix: 修复大运计算错误
docs: 更新 README 使用示例
test: 添加八字排盘单元测试
```

## 📋 开发环境设置

### Python 技能

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖（如有）
pip install -r requirements.txt

# 运行测试
python3 tests/test_*.py
```

### Node.js 技能

```bash
# 安装依赖（如有）
npm install

# 运行测试
npm test
```

## 🧪 测试

请为新功能添加测试用例！

### Python 测试示例

```python
# tests/test_feature.py
import unittest
from scripts.main_module import function

class TestFeature(unittest.TestCase):
    def test_function(self):
        result = function(input)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
```

## 📝 代码审查清单

提交前请自查：

- [ ] 代码通过所有测试
- [ ] 添加了必要的测试用例
- [ ] 代码符合规范（缩进、命名等）
- [ ] 更新了文档（README、CHANGELOG）
- [ ] 提交信息清晰规范
- [ ] 无调试代码（print、console.log 等）

## 💬 讨论

有问题或想法？欢迎创建 Issue 讨论！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

感谢你的贡献！🏮

**天工长老 敬上**
