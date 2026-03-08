

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "🚀 University Assignment Manager - Deployment Script" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "اختر طريقة النشر:" -ForegroundColor Yellow
Write-Host "1. بناء APK للموبايل فقط" -ForegroundColor Green
Write-Host "2. تشغيل Backend على الشبكة المحلية (Wi-Fi)" -ForegroundColor Green
Write-Host "3. بناء APK + تشغيل Backend معاً" -ForegroundColor Green
Write-Host "4. نشر باستخدام Docker" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "أدخل رقم الخيار (1-4)"

switch ($choice) {
    "1" {
        Write-Host "`n📦 جاري بناء APK..." -ForegroundColor Cyan
        
        Set-Location -Path "frontend"
        
        Write-Host "🔨 تشغيل flutter clean..." -ForegroundColor Yellow
        flutter clean
        
        Write-Host "📦 تشغيل flutter pub get..." -ForegroundColor Yellow
        flutter pub get
        
        Write-Host "🏗️ بناء APK Release..." -ForegroundColor Yellow
        flutter build apk --release
        
        Write-Host "`n✅ تم بناء APK بنجاح!" -ForegroundColor Green
        Write-Host "📍 الملف موجود في: build\app\outputs\flutter-apk\app-release.apk" -ForegroundColor Green
        
        $apkPath = "build\app\outputs\flutter-apk\app-release.apk"
        if (Test-Path $apkPath) {
            $size = (Get-Item $apkPath).Length / 1MB
            Write-Host "📊 حجم APK: $([math]::Round($size, 2)) MB" -ForegroundColor Cyan
        }
        
        Set-Location -Path ".."
    }
    
    "2" {
        Write-Host "`n🌐 جاري تشغيل Backend على الشبكة المحلية..." -ForegroundColor Cyan
        
        $localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*").IPAddress | Select-Object -First 1
        
        if (-not $localIP) {
            $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress | Select-Object -First 1
        }
        
        if ($localIP) {
            Write-Host "📍 عنوان IP المحلي: $localIP" -ForegroundColor Green
            Write-Host "🔗 سيكون API متاحاً على: http://${localIP}:8000" -ForegroundColor Green
            Write-Host ""
            Write-Host "⚠️  تذكر تحديث ApiConfig في التطبيق إلى:" -ForegroundColor Yellow
            Write-Host "   static const String baseUrl = 'http://${localIP}:8000';" -ForegroundColor Yellow
            Write-Host ""
        } else {
            Write-Host "⚠️  لم يتم العثور على IP محلي. تأكد من اتصالك بالشبكة." -ForegroundColor Red
        }
        
        Set-Location -Path "backend"
        
        Write-Host "🔌 تفعيل البيئة الافتراضية..." -ForegroundColor Yellow
        & "..\.venv\Scripts\Activate.ps1"
        
        Write-Host "🚀 تشغيل Backend..." -ForegroundColor Yellow
        Write-Host "   💡 للإيقاف: اضغط Ctrl+C" -ForegroundColor Cyan
        Write-Host ""
        
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    }
    
    "3" {
        Write-Host "`n🔄 سيتم بناء APK أولاً، ثم تشغيل Backend..." -ForegroundColor Cyan
        Write-Host ""
        
        Write-Host "📦 جاري بناء APK..." -ForegroundColor Cyan
        Set-Location -Path "frontend"
        flutter clean
        flutter pub get
        flutter build apk --release
        
        $apkPath = "build\app\outputs\flutter-apk\app-release.apk"
        if (Test-Path $apkPath) {
            Write-Host "✅ تم بناء APK بنجاح!" -ForegroundColor Green
        }
        
        Set-Location -Path ".."
        
        $localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*").IPAddress | Select-Object -First 1
        if (-not $localIP) {
            $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress | Select-Object -First 1
        }
        
        Write-Host ""
        Write-Host "🌐 جاري تشغيل Backend..." -ForegroundColor Cyan
        if ($localIP) {
            Write-Host "📍 API متاح على: http://${localIP}:8000" -ForegroundColor Green
        }
        
        Set-Location -Path "backend"
        & "..\.venv\Scripts\Activate.ps1"
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    }
    
    "4" {
        Write-Host "`n🐳 جاري النشر باستخدام Docker..." -ForegroundColor Cyan
        
        if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
            Write-Host "❌ Docker غير مثبت! حمّله من: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
            exit
        }
        
        Write-Host "🔨 بناء وتشغيل Container..." -ForegroundColor Yellow
        docker-compose up --build -d
        
        Write-Host ""
        Write-Host "✅ تم تشغيل Backend في Docker!" -ForegroundColor Green
        Write-Host "🔗 API متاح على: http://localhost:8000" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 للتحقق من الحالة: docker-compose ps" -ForegroundColor Cyan
        Write-Host "📋 لعرض Logs: docker-compose logs -f" -ForegroundColor Cyan
        Write-Host "🛑 للإيقاف: docker-compose down" -ForegroundColor Cyan
    }
    
    default {
        Write-Host "❌ خيار غير صحيح!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "✨ تم!" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Cyan
