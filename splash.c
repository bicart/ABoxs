#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// 资源ID定义
#define ID_TIMER 1

// 全局变量
HWND hWnd;
HBITMAP hBitmap = NULL;
int progress = 0;
BOOL pyStarted = FALSE;

// 加载图片
HBITMAP LoadImageFromFile(const WCHAR* filename) {
    return (HBITMAP)LoadImageW(NULL, filename, IMAGE_BITMAP, 0, 0, 
                               LR_LOADFROMFILE | LR_CREATEDIBSECTION);
}

// 绘制窗口
void DrawWindow(HWND hwnd) {
    PAINTSTRUCT ps;
    HDC hdc = BeginPaint(hwnd, &ps);
    HDC hdcMem = CreateCompatibleDC(hdc);
    
    // 获取窗口尺寸
    RECT rect;
    GetClientRect(hwnd, &rect);
    int width = rect.right - rect.left;
    int height = rect.bottom - rect.top;
    
    // 绘制背景色（渐变效果）
    for (int y = 0; y < height; y++) {
        //int r = 255, g = 255, b = 255;
        int r = 102, g = 126, b = 234;  // #667eea
        // 稍微调整颜色，制造渐变效果
        int adjust = (int)(y * 0.41);
        r = max(0, min(255, r - adjust));
        g = max(0, min(255, g - adjust));
        b = max(0, min(255, b + adjust));
        
        HBRUSH lineBrush = CreateSolidBrush(RGB(r, g, b));
        RECT lineRect = {0, y, width, y + 1};
        FillRect(hdc, &lineRect, lineBrush);
        DeleteObject(lineBrush);
    }
    
    // 绘制图片（自动缩放以适应窗口）
    if (hBitmap) {
        BITMAP bm;
        GetObject(hBitmap, sizeof(BITMAP), &bm);
        
        HGDIOBJ oldBitmap = SelectObject(hdcMem, hBitmap);
        
        // 计算缩放后的尺寸（保持宽高比）
        float scale;
        int targetWidth, targetHeight;
        
        // 图片尺寸：1052x237
        // 目标显示区域：窗口宽度80%，高度40%
        int maxWidth = (int)(width * 0.8);
        int maxHeight = (int)(height * 0.4);
        
        float widthScale = (float)maxWidth / bm.bmWidth;
        float heightScale = (float)maxHeight / bm.bmHeight;
        scale = min(widthScale, heightScale);
        
        targetWidth = (int)(bm.bmWidth * scale);
        targetHeight = (int)(bm.bmHeight * scale);
        
        // 居中显示
        int imgX = (width - targetWidth) / 2;
        int imgY = 30;
        
        // 使用StretchBlt缩放图片
        SetStretchBltMode(hdc, COLORONCOLOR);
        StretchBlt(hdc, imgX, imgY, targetWidth, targetHeight,
                  hdcMem, 0, 0, bm.bmWidth, bm.bmHeight, SRCCOPY);
        
        SelectObject(hdcMem, oldBitmap);
    } else {
        // 如果没有图片，绘制一个占位符
        HBRUSH whiteBrush = CreateSolidBrush(RGB(255, 255, 255));
        RECT imgRect = {150, 50, 250, 150};
        FillRect(hdc, &imgRect, whiteBrush);
        DeleteObject(whiteBrush);
    }
    
    // 设置字体为支持中文的
    SetTextColor(hdc, RGB(255, 255, 255));
    SetBkMode(hdc, TRANSPARENT);
    
    // 绘制标题（中文）
    HFONT hFont = CreateFontW(28, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE,
                             DEFAULT_CHARSET, OUT_DEFAULT_PRECIS,
                             CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY,
                             DEFAULT_PITCH | FF_DONTCARE, L"微软雅黑");
    HGDIOBJ oldFont = SelectObject(hdc, hFont);
    
    const WCHAR* title = L"ABoxs1.0 by bicart";
    RECT textRect = {0, (int)(height * 0.55), width, (int)(height * 0.55) + 40};
    DrawTextW(hdc, title, -1, &textRect, DT_CENTER | DT_VCENTER);
    
    SelectObject(hdc, oldFont);
    DeleteObject(hFont);
    
    // 绘制进度条背景
    int barWidth = 200;
    int barHeight = 8;
    int barX = (width - barWidth) / 2;
    int barY = (int)(height * 0.7);
    
    HBRUSH barBgBrush = CreateSolidBrush(RGB(170, 170, 170));
    RECT barBgRect = {barX, barY, barX + barWidth, barY + barHeight};
    FillRect(hdc, &barBgRect, barBgBrush);
    DeleteObject(barBgBrush);
    
    // 绘制进度条前景
    int progressWidth = (int)(barWidth * (progress / 100.0));
    HBRUSH barFgBrush = CreateSolidBrush(RGB(255, 255, 255));
    RECT barFgRect = {barX, barY, barX + progressWidth, barY + barHeight};
    FillRect(hdc, &barFgRect, barFgBrush);
    DeleteObject(barFgBrush);
    
    // 绘制进度文本（中文）
    hFont = CreateFontW(14, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
                       DEFAULT_CHARSET, OUT_DEFAULT_PRECIS,
                       CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY,
                       DEFAULT_PITCH | FF_DONTCARE, L"微软雅黑");
    SelectObject(hdc, hFont);
    
    WCHAR progressText[50];
    swprintf(progressText, 50, L"启动中... %d%%", progress);
    RECT progressRect = {0, (int)(height * 0.75), width, (int)(height * 0.75) + 30};
    DrawTextW(hdc, progressText, -1, &progressRect, DT_CENTER | DT_VCENTER);
    
    SelectObject(hdc, oldFont);
    DeleteObject(hFont);
    
    DeleteDC(hdcMem);
    EndPaint(hwnd, &ps);
}

// 窗口过程函数
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_CREATE:
            // 加载图片
            hBitmap = LoadImageFromFile(L"bicc.bmp");
            // 设置定时器，每30ms更新进度
            SetTimer(hwnd, ID_TIMER, 47, NULL);
            break;
            
        case WM_TIMER:
            if (progress < 100) {
                progress++;
                InvalidateRect(hwnd, NULL, TRUE);
                
                // 在70%进度时启动Python程序
                if (progress >= 70 && !pyStarted) {
                    pyStarted = TRUE;
                    // 启动Python程序
                    STARTUPINFOW si = {sizeof(si)};
                    PROCESS_INFORMATION pi;
                    
                    WCHAR cmdLine[] = L"python \"ABoxs-Bt38.py\"";
                    CreateProcessW(NULL, cmdLine, NULL, NULL, FALSE, 
                                  CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
                    CloseHandle(pi.hProcess);
                    CloseHandle(pi.hThread);
                }
            } else {
                // 进度完成，关闭窗口
                KillTimer(hwnd, ID_TIMER);
                DestroyWindow(hwnd);
            }
            break;
            
        case WM_PAINT:
            DrawWindow(hwnd);
            break;
            
        case WM_DESTROY:
            if (hBitmap) DeleteObject(hBitmap);
            PostQuitMessage(0);
            break;
            
        case WM_NCHITTEST:
            // 允许拖动无边框窗口
            return HTCAPTION;
            
        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
    return 0;
}

// 主函数
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, 
                   LPSTR lpCmdLine, int nCmdShow) {
    // 注册窗口类
    const WCHAR CLASS_NAME[] = L"SplashWindow";
    
    WNDCLASSW wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hbrBackground = NULL;  // 自定义绘制
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    
    RegisterClassW(&wc);
    
    // 创建窗口（无边框）
    hWnd = CreateWindowExW(
        WS_EX_TOOLWINDOW,      // 扩展样式：工具窗口，不在任务栏显示
        CLASS_NAME,
        L"",
        WS_POPUP,              // 无边框窗口
        CW_USEDEFAULT, CW_USEDEFAULT, 600, 350,  // 增大窗口尺寸以适应大图片
        NULL, NULL, hInstance, NULL
    );
    
    if (!hWnd) return 1;
    
    // 居中显示
    int screenWidth = GetSystemMetrics(SM_CXSCREEN);
    int screenHeight = GetSystemMetrics(SM_CYSCREEN);
    int windowWidth = 600, windowHeight = 350;
    SetWindowPos(hWnd, NULL, 
                 (screenWidth - windowWidth) / 2,
                 (screenHeight - windowHeight) / 2,
                 windowWidth, windowHeight, 0);
    
    // 显示窗口
    ShowWindow(hWnd, nCmdShow);
    UpdateWindow(hWnd);
    
    // 消息循环
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    return 0;
}