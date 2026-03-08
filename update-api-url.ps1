
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "🔧 تحديث API URL في التطبيق" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

$localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*").IPAddress | Select-Object -First 1

if (-not $localIP) {
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*"}).IPAddress | Select-Object -First 1
}

Write-Host "اختر نوع البيئة:" -ForegroundColor Yellow
Write-Host "1. Development (localhost)" -ForegroundColor Green
Write-Host "2. Local Network (Wi-Fi) - الموصى به للاختبار بدون USB" -ForegroundColor Green
Write-Host "3. Custom URL (أدخل عنوان مخصص)" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "أدخل رقم الخيار (1-3)"

$newUrl = ""

switch ($choice) {
    "1" {
        $newUrl = "http://127.0.0.1:8000"
        Write-Host "✅ سيتم استخدام: $newUrl" -ForegroundColor Green
    }
    
    "2" {
        if ($localIP) {
            $newUrl = "http://${localIP}:8000"
            Write-Host "✅ تم اكتشاف IP المحلي: $localIP" -ForegroundColor Green
            Write-Host "✅ سيتم استخدام: $newUrl" -ForegroundColor Green
        } else {
            Write-Host "❌ لم يتم العثور على IP محلي!" -ForegroundColor Red
            $manualIP = Read-Host "أدخل IP يدوياً (مثال: 192.168.1.100)"
            $newUrl = "http://${manualIP}:8000"
        }
    }
    
    "3" {
        $customUrl = Read-Host "أدخل عنوان API الكامل (مثال: https://api.example.com)"
        $newUrl = $customUrl
        Write-Host "✅ سيتم استخدام: $newUrl" -ForegroundColor Green
    }
    
    default {
        Write-Host "❌ خيار غير صحيح!" -ForegroundColor Red
        exit
    }
}

Write-Host ""
Write-Host "🔄 جاري تحديث ملف ApiConfig..." -ForegroundColor Yellow

$configPath = "frontend\lib\core\api\api_config.dart"

$newContent = @"
class ApiConfig {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '$newUrl',
  );
}
"@

Set-Content -Path $configPath -Value $newContent -Encoding UTF8

Write-Host "✅ تم تحديث ApiConfig بنجاح!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 المحتوى الجديد:" -ForegroundColor Cyan
Write-Host "$newContent" -ForegroundColor White
Write-Host ""
Write-Host "💡 الآن يمكنك بناء APK بتشغيل:" -ForegroundColor Yellow
Write-Host "   cd frontend" -ForegroundColor White
Write-Host "   flutter build apk --release" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  تذكر: يجب أن يكون Backend يعمل على العنوان الذي اخترته!" -ForegroundColor Yellow

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "✨ تم!" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Cyan
