<!DOCTYPE html>
<html>
<#include "/header.ftl">
<body>
<#include "/navbar.ftl">

<#if name=="ireul">
hello ${name}(${age})
<#else>
fuck ${name}(${age})
</#if>

</body>
</html>