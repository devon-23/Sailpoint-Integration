# API Integration Examples and Quick Reference

## Table of Contents
1. [API Endpoint Configuration](#api-endpoint-configuration)
2. [Request/Response Examples](#requestresponse-examples)
3. [Common Scenarios](#common-scenarios)
4. [Error Responses](#error-responses)

---

## API Endpoint Configuration

### REST Endpoint
```
POST /identityiq/api/workflow/execute
```

### Authentication
- **Type**: Bearer Token
- **Header**: `Authorization: Bearer {TOKEN}`
- **Token Acquisition**: Get from IIQ API Management console

### Content Type
```
Content-Type: application/json
```

---

## Request/Response Examples

### Example 1: Basic Group Creation

**Request:**
```json
{
  "workflowName": "Create AD Group from API",
  "workflowParams": {
    "applicationName": "Active Directory",
    "groupName": "DEPT-Engineering",
    "groupDescription": "Engineering Department Group",
    "groupOwner": "CN=Admin User,OU=Service Accounts,DC=company,DC=com",
    "groupType": "Security",
    "groupScope": "Global",
    "organizationalUnit": "OU=Department Groups,OU=Applications,DC=company,DC=com"
  }
}
```

**Success Response (200 OK):**
```json
{
  "requestId": "550e8400-e29b-41d4-a716-446655440000",
  "isSuccess": true,
  "errorMessage": null,
  "workflowId": "flow-12345",
  "duration": 3250
}
```

---

### Example 2: Group with Email and Additional Attributes

**Request:**
```json
{
  "workflowName": "Create AD Group from API",
  "workflowParams": {
    "applicationName": "Active Directory",
    "groupName": "PROJ-DataPlatform",
    "groupDescription": "Data Platform Project Group",
    "groupOwner": "CN=Project Manager,OU=Users,DC=company,DC=com",
    "groupType": "Distribution",
    "groupScope": "Universal",
    "organizationalUnit": "OU=Project Groups,OU=Applications,DC=company,DC=com",
    "groupEmail": "data-platform-team@company.com",
    "additionalAttributes": {
      "info": "Created for data platform project",
      "notes": "Project ID: PROJ-2024-001",
      "wWWHomePage": "https://confluence.company.com/data-platform"
    }
  }
}
```

**Success Response:**
```json
{
  "requestId": "660f9511-f40c-52e5-b827-557766551111",
  "isSuccess": true,
  "errorMessage": null,
  "workflowId": "flow-12346",
  "duration": 4120
}
```

---

### Example 3: Distribution List for Email

**Request:**
```json
{
  "workflowName": "Create AD Group from API",
  "workflowParams": {
    "applicationName": "Active Directory",
    "groupName": "AllHandsMeeting",
    "groupDescription": "All Hands Meeting Distribution List",
    "groupOwner": "CN=HR Manager,OU=Users,DC=company,DC=com",
    "groupType": "Distribution",
    "groupScope": "Universal",
    "organizationalUnit": "OU=Distribution Lists,DC=company,DC=com",
    "groupEmail": "all-hands@company.com"
  }
}
```

---

## Common Scenarios

### Scenario 1: Security Group for Application Access

```json
{
  "workflowName": "Create AD Group from API",
  "workflowParams": {
    "applicationName": "Active Directory",
    "groupName": "APP-Salesforce-Users",
    "groupDescription": "Salesforce application access group",
    "groupOwner": "CN=Salesforce Admin,OU=Admins,DC=company,DC=com",
    "groupType": "Security",
    "groupScope": "Global",
    "organizationalUnit": "OU=Application Groups,OU=Groups,DC=company,DC=com",
    "additionalAttributes": {
      "info": "Salesforce access control",
      "notes": "Managed by Salesforce Admin team"
    }
  }
}
```

**Use Case**: Control access to Salesforce application via AD group membership

---

### Scenario 2: Department Resource Group

```json
{
  "workflowName": "Create AD Group from API",
  "workflowParams": {
    "applicationName": "Active Directory",
    "groupName": "DEPT-Marketing-Resources",
    "groupDescription": "Marketing Department Resource Access",
    "groupOwner": "CN=Marketing Director,OU=Users,DC=company,DC=com",
    "groupType": "Security",
    "groupScope": "Global",
    "organizationalUnit": "OU=Department Groups,OU=Groups,DC=company,DC=com",
    "additionalAttributes": {
      "info": "Marketing department file share access",
      "notes": "Manage through marketing manager approval"
    }
  }
}
```

**Use Case**: Control access to shared resources for a department

---

### Scenario 3: Project Team Distribution List

```json
{
  "workflowName": "Create AD Group from API",
  "workflowParams": {
    "applicationName": "Active Directory",
    "groupName": "PROJ-CloudMigration-Team",
    "groupDescription": "Cloud Migration Initiative Team",
    "groupOwner": "CN=Project Lead,OU=Users,DC=company,DC=com",
    "groupType": "Distribution",
    "groupScope": "Universal",
    "organizationalUnit": "OU=Project Groups,DC=company,DC=com",
    "groupEmail": "cloud-migration-team@company.com"
  }
}
```

**Use Case**: Email distribution for project team communications

---

### Scenario 4: Nested Organization Structure

```json
{
  "workflowName": "Create AD Group from API",
  "workflowParams": {
    "applicationName": "Active Directory",
    "groupName": "ACME-Corp-Engineering-Backend",
    "groupDescription": "Backend Engineering Team - ACME Corp Division",
    "groupOwner": "CN=Engineering Manager,OU=Management,OU=ACME,DC=company,DC=com",
    "groupType": "Security",
    "groupScope": "Global",
    "organizationalUnit": "OU=Engineering,OU=ACME Division,OU=Groups,DC=company,DC=com",
    "additionalAttributes": {
      "division": "ACME",
      "department": "Engineering",
      "team": "Backend"
    }
  }
}
```

**Use Case**: Groups organized in nested OU structure for large organizations

---

## Error Responses

### Error 1: Missing Required Parameter

**Request (missing groupOwner):**
```json
{
  "workflowName": "Create AD Group from API",
  "workflowParams": {
    "applicationName": "Active Directory",
    "groupName": "TestGroup",
    "groupDescription": "Test",
    "groupType": "Security",
    "groupScope": "Global",
    "organizationalUnit": "OU=Groups,DC=company,DC=com"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "requestId": "770g0622-g51d-63f6-c938-668877662222",
  "isSuccess": false,
  "errorMessage": "Validation Failed: [groupOwner is required]",
  "workflowId": null,
  "duration": 450
}
```

---

### Error 2: Invalid Enum Value

**Request (invalid groupType):**
```json
{
  "workflowParams": {
    "applicationName": "Active Directory",
    "groupName": "TestGroup",
    "groupDescription": "Test",
    "groupOwner": "CN=User,DC=company,DC=com",
    "groupType": "Special",
    "groupScope": "Global",
    "organizationalUnit": "OU=Groups,DC=company,DC=com"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "requestId": "880h0733-h62e-74g7-d049-779988773333",
  "isSuccess": false,
  "errorMessage": "Validation Failed: [groupType must be either 'Security' or 'Distribution']",
  "workflowId": null,
  "duration": 320
}
```

---

### Error 3: Application Not Found

**Request (invalid application name):**
```json
{
  "workflowParams": {
    "applicationName": "NonExistent-Directory",
    "groupName": "TestGroup",
    "groupDescription": "Test",
    "groupOwner": "CN=User,DC=company,DC=com",
    "groupType": "Security",
    "groupScope": "Global",
    "organizationalUnit": "OU=Groups,DC=company,DC=com"
  }
}
```

**Response (404 Not Found):**
```json
{
  "requestId": "990i0844-i73f-85h8-e15a-8809999884444",
  "isSuccess": false,
  "errorMessage": "Active Directory application not found: NonExistent-Directory",
  "workflowId": "flow-12347",
  "duration": 780
}
```

---

### Error 4: Connector Error (Permissions)

**Scenario**: OU path doesn't exist or insufficient permissions

**Response (500 Server Error):**
```json
{
  "requestId": "aa0j0955-j84g-96i9-f26b-9910aaa0aa555",
  "isSuccess": false,
  "errorMessage": "Error executing provisioning: Access to AD OU is denied",
  "workflowId": "flow-12348",
  "duration": 2100
}
```

---

### Error 5: Multiple Validation Errors

**Request (multiple issues):**
```json
{
  "workflowParams": {
    "applicationName": "",
    "groupName": "",
    "groupDescription": "Test",
    "groupOwner": "",
    "groupType": "Invalid",
    "groupScope": "BadScope",
    "organizationalUnit": ""
  }
}
```

**Response (400 Bad Request):**
```json
{
  "requestId": "bb0k1066-k95h-a7j0-g37c-aa11bbb1bb666",
  "isSuccess": false,
  "errorMessage": "Validation Failed: [applicationName is required, groupName is required, groupOwner is required, groupType must be either 'Security' or 'Distribution', groupScope must be 'Global', 'Domain Local', or 'Universal', organizationalUnit is required]",
  "workflowId": null,
  "duration": 320
}
```

---

## Response Codes Summary

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Group created successfully |
| 400 | Bad Request | Missing or invalid parameters |
| 401 | Unauthorized | Invalid/missing API token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Application doesn't exist |
| 500 | Internal Error | AD connector error, network issue |
| 503 | Service Unavailable | IIQ or AD server down |

---

## Testing the API

### Using Postman

1. Create new POST request
2. Set URL: `https://your-iiq-host/identityiq/api/workflow/execute`
3. Authorization Tab:
   - Type: Bearer Token
   - Token: `YOUR_API_TOKEN`
4. Body Tab:
   - Select "raw" and "JSON"
   - Paste request JSON
5. Send request

### Using cURL

```bash
curl -X POST "https://your-iiq-host/identityiq/api/workflow/execute" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d @request.json -v
```

### Using Insomnia

1. New request → POST
2. URL: `https://your-iiq-host/identityiq/api/workflow/execute`
3. Auth: Bearer Token → `YOUR_API_TOKEN`
4. Body: JSON raw mode
5. Send

---

## Monitoring and Logging

### Check Workflow Execution
- Navigate to: IIQ Admin Console → Workflows → Execution History
- Filter by workflow name: "Create AD Group from API"
- Look for execution duration and status

### Check Audit Trail
- Navigate to: IIQ Admin Console → Audit Trail
- Search for action "CreateADGroup"
- View request ID, timestamp, and parameters

### Check AD
- Open Active Directory Users and Computers
- Search for group by name
- Verify group properties match request

---

## Rate Limiting

- **Default**: 100 requests per hour per API token
- **Contact**: IIQ Admin to adjust rate limits
- **Retry Logic**: Implement exponential backoff on 503 responses

---

## Best Practices

1. **Always validate parameters** before sending request
2. **Store request ID** for tracking and troubleshooting
3. **Implement retry logic** with exponential backoff
4. **Log all API calls** for audit trail
5. **Use meaningful group names** with clear prefixes
6. **Always assign valid group owners**
7. **Test in non-production** first
8. **Monitor execution times** for performance issues

---
