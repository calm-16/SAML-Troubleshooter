# SAML Troubleshooter Agent - AG2 模块化设计

## 1. ConversableAgent（对话式 Agent）
**角色**：核心智能体，接收输入并生成分析  
**功能**：
- 接收用户输入（报错信息、SAMLResponse、HTTP 抓包等）
- 调用 LLM 分析错误类型
- 提供初步诊断和可能原因列表

**示例交互**：

User: "SAML login fails with 'Invalid Signature'"

Agent: "Detected possible signature issue, checking SP and IdP certificates..."

---

## 2. Human in the Loop (HITL)
**角色**：在关键或模糊点引入人工确认  
**功能**：
- 当 Agent 不能确定根因时，请求用户提供更多信息
- 让用户从多种可能原因中选择最合适的一条
- 平衡自动化与人工判断

**示例**：

Agent: "Could be SP certificate expired or IdP metadata outdated. Please confirm which applies."

User: "SP certificate expired."


---

## 3. Agent Orchestration（Agent 编排）
**角色**：定义诊断流程和多 Agent 协作模式  
**步骤**：
1. **输入收集**：日志、SAMLResponse、用户描述
2. **格式/Schema 检查**：验证 XML 结构、签名
3. **协议流检查**：检查 SP → IdP → SP 流程是否完成
4. **问题分类**：证书 / 配置 / 时钟 / 网络
5. **修复建议**：生成建议列表和操作指引

---

## 4. Tools（工具调用）
**角色**：扩展 Agent 能力，执行实际检测  
**工具示例**：
- XML parser → 验证 SAMLResponse 结构
- Signature validator → 检查证书签名
- Clock checker → 验证 `NotBefore` / `NotOnOrAfter` 时间
- Metadata parser → 提取 IdP/SP 配置
- Log search API → 查询系统日志

---

## 5. Structured Outputs（结构化输出）
**角色**：标准化诊断报告，方便下游处理  
**功能**：
- 定义统一输出格式
- 保证输出字段完整、可验证
- 提供明确修复建议

**示例 JSON 输出**：
```json
{
  "transaction_id": "abc123",
  "status": "error_detected",
  "error_type": "invalid_signature",
  "possible_causes": [
    "SP certificate expired",
    "IdP metadata outdated"
  ],
  "recommendations": [
    "Update SP certificate",
    "Re-import IdP metadata"
  ]
}
