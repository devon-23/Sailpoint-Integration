# SailPoint IIQ: Create AD Group from API - Implementation Guide

## Overview

This workflow is designed to create Active Directory groups programmatically via API calls. It handles validation, group creation, and audit logging with comprehensive error handling.

---

## Workflow Architecture

### Input Parameters

The workflow accepts the following parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `applicationName` | String | Yes | Name of the AD application configured in IIQ |
| `groupName` | String | Yes | Name of the AD group to create (sAMAccountName) |
| `groupDescription` | String | Yes | Description of the group |
| `groupOwner` | String | Yes | DN or name of the user who will manage the group |
| `groupType` | String | Yes | Type of group: `Security` or `Distribution` |
| `groupScope` | String | Yes | Scope: `Global`, `Domain Local`, or `Universal` |
| `organizationalUnit` | String | Yes | LDAP DN path where group will be created |
| `groupEmail` | String | No | Email address for the group (optional) |
| `additionalAttributes` | Map | No | Additional AD attributes as key-value pairs |

---

## Workflow Steps

### 1. **ValidateInput**
- Validates all required parameters
- Checks for empty/null values
- Validates enum values (groupType, groupScope)
- Returns error list if validation fails

### 2. **GetADApplication**
- Retrieves the AD application object from IIQ
- Verifies the application exists
- Fails gracefully if application not found

### 3. **BuildProvisioningPlan**
- Creates a ProvisioningPlan with account creation request
- Maps input parameters to AD attributes
- Supports additional custom attributes
- Handles group type encoding (Security/Distribution)

### 4. **ExecuteProvisioning**
- Gets the connector from the AD application
- Executes the provisioning plan against the connector
- Handles connector-level errors

### 5. **LogAudit**
- Creates audit event with request details
- Logs execution duration
- Stores request tracking information

### 6. **HandleError**
- Captures and logs error messages
- Provides error information in workflow output

---

## API Call Examples

### Using cURL

```bash
curl -X POST https://your-sailpoint-host/identityiq/api/workflow/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{
    "workflowName": "Create AD Group from API",
    "workflowParams": {
      "applicationName": "Active Directory",
      "groupName": "APP-Sales-Group",
      "groupDescription": "Sales Department Application Group",
      "groupOwner": "CN=John Doe,OU=Users,DC=company,DC=com",
      "groupType": "Security",
      "groupScope": "Global",
      "organizationalUnit": "OU=Applications,OU=Groups,DC=company,DC=com",
      "groupEmail": "app-sales-group@company.com",
      "additionalAttributes": {
        "notes": "Created via API",
        "info": "Sales team group"
      }
    }
  }'
```

### Using Java/REST Client

```java
Map<String, Object> params = new HashMap<>();
params.put("applicationName", "Active Directory");
params.put("groupName", "APP-Finance-Group");
params.put("groupDescription", "Finance Department Group");
params.put("groupOwner", "CN=Jane Smith,OU=Users,DC=company,DC=com");
params.put("groupType", "Security");
params.put("groupScope", "Global");
params.put("organizationalUnit", "OU=Applications,OU=Groups,DC=company,DC=com");
params.put("groupEmail", "app-finance@company.com");

Map<String, Object> additionalAttrs = new HashMap<>();
additionalAttrs.put("info", "Finance team");
params.put("additionalAttributes", additionalAttrs);

workflowClient.executeWorkflow("Create AD Group from API", params);
```

### Using Python

```python
import requests
import json

url = "https://your-sailpoint-host/identityiq/api/workflow/execute"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_TOKEN"
}

payload = {
    "workflowName": "Create AD Group from API",
    "workflowParams": {
        "applicationName": "Active Directory",
        "groupName": "APP-HR-Group",
        "groupDescription": "Human Resources Department Group",
        "groupOwner": "CN=Bob Wilson,OU=Users,DC=company,DC=com",
        "groupType": "Security",
        "groupScope": "Global",
        "organizationalUnit": "OU=Applications,OU=Groups,DC=company,DC=com",
        "groupEmail": "app-hr@company.com",
        "additionalAttributes": {
            "info": "HR department"
        }
    }
}

response = requests.post(url, json=payload, headers=headers)
result = response.json()
print(f"Request ID: {result['requestId']}")
print(f"Success: {result['isSuccess']}")
```

---

## Output Variables

The workflow returns the following:

| Variable | Type | Description |
|----------|------|-------------|
| `requestId` | String | Unique identifier for this request |
| `isSuccess` | Boolean | Whether the operation succeeded |
| `errorMessage` | String | Error details if operation failed |
| `auditLog` | String | Summary of the action taken |

---

## Configuration Requirements

### 1. **Active Directory Application Setup**

The AD application must be configured in IIQ with:
- Valid connector (e.g., Active Directory connector)
- Proper authentication credentials
- Network connectivity to AD infrastructure

### 2. **Permissions**

The IIQ service account needs:
- Permission to create groups in the specified OU
- Ability to set group properties
- Permission to assign group owners

### 3. **Required Attributes**

Ensure AD connector supports the following attributes:
- sAMAccountName
- cn
- displayName
- description
- groupType
- groupScope
- ou
- managedBy
- mail

---

## Error Handling

The workflow handles errors at multiple levels:

### Validation Errors
- Missing required parameters
- Invalid enum values
- Empty string inputs

### Application Errors
- Application not found in IIQ
- Connector unavailable

### Provisioning Errors
- AD connectivity issues
- Permission denied on OU
- Group already exists

All errors are logged and returned in the `errorMessage` variable.

---

## Advanced Usage

### Creating Groups in Different OUs

Pass different OU paths for different group types:

```json
{
  "organizationalUnit": "OU=Security-Groups,OU=Applications,DC=company,DC=com"
}
```

### Adding Custom Attributes

Use the `additionalAttributes` map to add any AD attributes:

```json
{
  "additionalAttributes": {
    "info": "Custom info",
    "notes": "Some notes",
    "wWWHomePage": "https://app.example.com"
  }
}
```

### Distribution Lists

To create a distribution list instead of a security group:

```json
{
  "groupType": "Distribution",
  "groupScope": "Universal"
}
```

---

## Security Considerations

1. **API Authentication**: Use strong authentication tokens for API calls
2. **Input Validation**: All inputs are validated; no SQL injection is possible
3. **Audit Logging**: All group creations are logged with timestamps and request IDs
4. **Credentials**: Ensure the IIQ service account has minimal necessary permissions
5. **Group Ownership**: Always assign a valid owner for access control

---

## Troubleshooting

### Issue: "Active Directory application not found"
**Solution**: Verify the application name matches exactly in IIQ configuration. Check capitalization.

### Issue: "Permission denied" error
**Solution**: Verify the IIQ service account has permissions in the specified OU. Check AD security.

### Issue: Group creation times out
**Solution**: Check network connectivity to AD server. Increase timeout values if needed.

### Issue: Invalid group type error
**Solution**: Ensure groupType is either "Security" or "Distribution" (case-sensitive).

### Issue: Invalid scope error
**Solution**: Ensure groupScope is one of: "Global", "Domain Local", or "Universal" (case-sensitive).

---

## Performance Considerations

- Provisioning execution time depends on AD server response times
- Typical creation time: 2-5 seconds
- Audit logging adds minimal overhead (~100ms)
- Connector pooling improves performance for high-volume requests

---

## Maintenance and Monitoring

### Monitor These Logs
- IIQ system logs for workflow execution
- AD event logs for group creation
- IIQ audit trail for API calls

### Regular Checks
- Verify group properties after creation
- Validate group ownership assignments
- Monitor failed API requests

---

## Extended Functionality Ideas

The workflow can be extended to:
- Add users to groups after creation
- Send notifications on group creation
- Create related distribution lists
- Assign group permissions automatically
- Integrate with service catalogs

---

## Support and Questions

For issues or questions:
1. Check the audit logs in IIQ (Admin Console → Audit Trail)
2. Review the workflow execution history
3. Check IIQ system logs for detailed errors
4. Verify AD application configuration
5. Test connectivity to AD separately

---

## Version History

- **v1.0** - Initial release
- Supports single group creation
- Includes comprehensive validation
- Full audit logging

---
