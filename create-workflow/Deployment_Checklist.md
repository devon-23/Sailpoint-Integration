# SailPoint IIQ AD Group Workflow - Deployment Checklist

## Pre-Deployment Requirements

### Infrastructure Setup
- [ ] SailPoint IIQ 8.x or higher installed
- [ ] IIQ server is running and accessible
- [ ] Active Directory infrastructure is operational
- [ ] Network connectivity between IIQ and AD servers verified
- [ ] Sufficient disk space on IIQ server (>2GB recommended)

### Access and Credentials
- [ ] IIQ Admin credentials available
- [ ] AD service account created with group creation permissions
- [ ] API authentication token generated
- [ ] Database backup taken before deployment

---

## Step 1: Import Workflow

### Via IIQ Admin Console

1. [ ] Log in to IIQ Admin Console
2. [ ] Navigate to: **Workflows** → **Import**
3. [ ] Browse and select `CreateADGroupWorkflow.xml`
4. [ ] Click **Import**
5. [ ] Verify no import errors
6. [ ] Note the workflow ID

### Via CLI/API (Alternative)

```bash
./iiq.sh import -f CreateADGroupWorkflow.xml -t workflow
```

- [ ] Verify import succeeded
- [ ] Check logs for any warnings

---

## Step 2: Configure AD Application

### Verify AD Application Exists

1. [ ] Log in to IIQ Admin Console
2. [ ] Navigate to: **System Configuration** → **Applications**
3. [ ] Verify "Active Directory" application exists
4. [ ] If not, create new application:
   - [ ] Name: `Active Directory`
   - [ ] Type: Select appropriate AD connector
   - [ ] Configure connector with:
     - [ ] AD server hostname
     - [ ] Port (usually 389 for LDAP, 636 for LDAPS)
     - [ ] Service account credentials
     - [ ] Base DN
     - [ ] Connection pool settings

### Test AD Connection

```bash
# In IIQ shell or via test script
context = new Context(server, sailpoint.object.SailPointContext);
app = context.getObjectByName(sailpoint.object.Application.class, "Active Directory");
connector = app.getConnector();
// If no error, connection is valid
```

- [ ] Connection test passed
- [ ] Log in messages show successful authentication

---

## Step 3: Configure Service Account Permissions

### AD Service Account Requirements

The IIQ service account needs these permissions:

1. [ ] **Create Group Objects**
   ```
   Right: Create all child objects
   Scope: The target OU (e.g., OU=Applications,DC=company,DC=com)
   ```

2. [ ] **Modify Group Properties**
   ```
   Right: Write all properties
   Scope: The target OU and below
   ```

3. [ ] **Set Group Owner/Manager**
   ```
   Right: Write managedBy property
   Scope: The target OU and below
   ```

### Verify Permissions

```powershell
# In PowerShell as AD Admin
$OU = "OU=Applications,OU=Groups,DC=company,DC=com"
$Account = "DOMAIN\iiq-service-account"

# List current permissions
(Get-Acl "AD:\$OU").Access | 
  Where-Object {$_.IdentityReference -like "*$Account*"} |
  Format-Table -Property IdentityReference, ActiveDirectoryRights, InheritanceType
```

- [ ] Service account has Create Child Objects permission
- [ ] Service account has Write All Properties permission
- [ ] Permissions include OU scope and descendants

---

## Step 4: Configure API Access

### Generate API Token

1. [ ] Log in to IIQ as Administrator
2. [ ] Navigate to: **Administration** → **System Configuration** → **API Management**
3. [ ] Create new API Client:
   - [ ] Name: `AD Group Creation API`
   - [ ] Type: `REST`
   - [ ] Authentication: `OAuth2 Bearer Token` or `API Key`
4. [ ] Configure scopes/permissions:
   - [ ] `workflow:execute`
   - [ ] `workflow:read`
5. [ ] Generate token
6. [ ] Copy token (will not be shown again)

### Create OAuth2 Client (If Using OAuth2)

```bash
# Configuration in IIQ properties
identityiq.rest.api.enabled = true
identityiq.rest.api.allowedScopes = workflow:execute,workflow:read
```

- [ ] API endpoint is accessible
- [ ] Token is valid and not expired
- [ ] Token has required scopes

---

## Step 5: Test Workflow Execution

### Test via IIQ Console

1. [ ] Log in to IIQ Admin Console
2. [ ] Navigate to: **Workflows** → **Create AD Group from API**
3. [ ] Click **Execute**
4. [ ] Fill in test parameters:
   ```
   applicationName: Active Directory
   groupName: TEST-Group-01
   groupDescription: Test group for validation
   groupOwner: CN=Admin,OU=Users,DC=company,DC=com
   groupType: Security
   groupScope: Global
   organizationalUnit: OU=Applications,OU=Groups,DC=company,DC=com
   ```
5. [ ] Click **Execute Workflow**
6. [ ] Wait for completion
7. [ ] Verify in results:
   - [ ] `isSuccess: true`
   - [ ] `requestId` is populated
   - [ ] No `errorMessage`

### Verify Group in AD

```powershell
# In PowerShell on AD server
Get-ADGroup -Identity "TEST-Group-01" | Format-List

# Check properties
Get-ADGroup "TEST-Group-01" -Properties * | 
  Select-Object Name, Description, GroupScope, GroupCategory, ManagedBy
```

- [ ] Group exists in AD
- [ ] Properties match request
- [ ] Owner is set correctly

### Test via API

```bash
curl -X POST "https://your-iiq-host/identityiq/api/workflow/execute" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{
    "workflowName": "Create AD Group from API",
    "workflowParams": {
      "applicationName": "Active Directory",
      "groupName": "API-Test-Group",
      "groupDescription": "Group created via API test",
      "groupOwner": "CN=Admin,OU=Users,DC=company,DC=com",
      "groupType": "Security",
      "groupScope": "Global",
      "organizationalUnit": "OU=Applications,OU=Groups,DC=company,DC=com"
    }
  }'
```

- [ ] API returns 200 OK
- [ ] Response shows `"isSuccess": true`
- [ ] Group is created in AD
- [ ] Audit log shows the creation

---

## Step 6: Security Hardening

### API Security

- [ ] API tokens have expiration dates set (e.g., 90 days)
- [ ] Tokens are stored securely (encrypted in password manager)
- [ ] API endpoints are HTTPS only (no HTTP)
- [ ] Rate limiting is configured (suggest: 100 req/hour)
- [ ] API access is logged and monitored

### Workflow Security

- [ ] Workflow is not publicly accessible
- [ ] Only authorized users can execute workflow
- [ ] Service account has minimal necessary permissions
- [ ] Workflow parameters are validated and sanitized
- [ ] Audit logging is enabled

### AD Security

- [ ] Service account password is complex (>20 characters)
- [ ] Service account is a standard user (not admin)
- [ ] Service account has time-based access restrictions if possible
- [ ] AD events are logged (4720 - Group Created, 4742 - Group Member Added)
- [ ] OU structure provides adequate isolation

---

## Step 7: Monitoring and Alerting

### Configure Workflow Monitoring

1. [ ] Set up alerts for failed executions
2. [ ] Configure email notifications to admins
3. [ ] Set up dashboard to track:
   - [ ] Total groups created (weekly/monthly)
   - [ ] Failed creation attempts
   - [ ] Average execution time
   - [ ] API error rates

### Configure Audit Trail

1. [ ] Audit trail logging is enabled
2. [ ] Configure retention (suggest: 1 year)
3. [ ] Set up automated reports:
   - [ ] Weekly group creation summary
   - [ ] Monthly access and usage report
   - [ ] Quarterly security review

### Example Monitoring Query

```sql
-- SQL query to monitor workflow executions (in IIQ database)
SELECT 
  action,
  action_time,
  status,
  COUNT(*) as count,
  AVG(DATEDIFF(second, action_time, completion_time)) as avg_duration_sec
FROM audit_event
WHERE action = 'CreateADGroup'
  AND action_time > DATEADD(day, -7, GETDATE())
GROUP BY action, action_time, status
ORDER BY action_time DESC;
```

- [ ] Monitoring dashboard is operational
- [ ] Alerts are configured
- [ ] Audit logs are being collected

---

## Step 8: Documentation and Training

### Documentation

- [ ] Implementation Guide is shared with team
- [ ] API Examples document is available
- [ ] Troubleshooting guide is documented
- [ ] Change log is maintained

### Team Training

- [ ] Operations team is trained on:
  - [ ] Workflow execution
  - [ ] Troubleshooting common errors
  - [ ] Monitoring and alerting
  - [ ] Emergency procedures

- [ ] Developers are trained on:
  - [ ] API authentication
  - [ ] Request format and parameters
  - [ ] Error handling and retry logic
  - [ ] Security best practices

- [ ] Documentation is in wiki/knowledge base
- [ ] Runbooks are created for on-call support

---

## Step 9: Performance Baseline

### Establish Baseline Metrics

- [ ] Single execution time: _____ ms (Target: <5 seconds)
- [ ] 10 concurrent executions: _____ ms
- [ ] 100 consecutive executions: _____ ms
- [ ] Peak throughput: _____ groups/minute

### Load Testing

```bash
#!/bin/bash
# Simple load test script
for i in {1..10}; do
  curl -X POST "https://your-iiq-host/identityiq/api/workflow/execute" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer YOUR_API_TOKEN" \
    -d "{...}" &
done
wait
```

- [ ] Load test completed successfully
- [ ] No errors under peak load
- [ ] Response times are acceptable
- [ ] System resources (CPU, memory) are healthy

---

## Step 10: Production Deployment

### Pre-Production Checklist

- [ ] All above steps completed and verified
- [ ] Code review completed
- [ ] Security audit passed
- [ ] Performance testing passed
- [ ] User acceptance testing (UAT) approved
- [ ] Rollback plan is documented

### Production Deployment

1. [ ] Schedule maintenance window (if needed)
2. [ ] Create database backup
3. [ ] Import workflow to production
4. [ ] Configure API access in production
5. [ ] Run smoke tests
6. [ ] Enable monitoring and alerts
7. [ ] Notify stakeholders of availability
8. [ ] Document deployment details

### Post-Deployment Verification

- [ ] API endpoint is accessible
- [ ] Test execution completes successfully
- [ ] Audit logs show execution
- [ ] Group is created in AD
- [ ] Monitoring dashboard is operational
- [ ] No errors in system logs

---

## Step 11: Rollback Plan

### If Issues Occur

1. [ ] Stop accepting new API requests
2. [ ] Delete any partially created groups
3. [ ] Review error logs for root cause
4. [ ] Document the issue
5. [ ] Options:
   - [ ] Fix and redeploy
   - [ ] Rollback to previous workflow version
   - [ ] Revert to manual group creation process

### Rollback Procedure

```bash
# Deactivate workflow in production
./iiq.sh> 
  Workflow w = context.getObjectByName(Workflow.class, "Create AD Group from API");
  w.setEnabled(false);
  context.saveObject(w);
  context.commitTransaction();
```

- [ ] Rollback procedure documented
- [ ] Rollback time estimate: _____ minutes
- [ ] Backup available and tested

---

## Ongoing Maintenance

### Weekly Tasks
- [ ] Review execution logs for errors
- [ ] Monitor performance metrics
- [ ] Check API error rates

### Monthly Tasks
- [ ] Review and update documentation
- [ ] Analyze usage trends
- [ ] Verify audit logs are being collected
- [ ] Check security updates for IIQ

### Quarterly Tasks
- [ ] Performance tuning review
- [ ] Security audit of API tokens
- [ ] Review and update runbooks
- [ ] Disaster recovery testing

### Annual Tasks
- [ ] Full security assessment
- [ ] Capacity planning
- [ ] Technology update assessment
- [ ] Renewal of API tokens

---

## Sign-Off

- [ ] Workflow Developer: _________________ Date: _______
- [ ] QA Lead: _________________ Date: _______
- [ ] Security Lead: _________________ Date: _______
- [ ] Operations Lead: _________________ Date: _______
- [ ] Project Manager: _________________ Date: _______

---

## Support Contacts

| Role | Name | Contact | Available |
|------|------|---------|-----------|
| IIQ Admin | | | |
| AD Administrator | | | |
| Network Support | | | |
| Security Team | | | |
| On-Call Support | | | |

---

## Notes and Issues Log

```
Date: _________
Issue: _________________________________
Resolution: _____________________________
Impact: _________________________________

Date: _________
Issue: _________________________________
Resolution: _____________________________
Impact: _________________________________
```

---
