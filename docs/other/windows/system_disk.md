# 系统盘空间抢救方案

## 📌 背景

应用经常把**缓存/配置/日志**硬编码写入 `%APPDATA%` 或 `%LOCALAPPDATA%`，即使你改了部分设置，仍会残留大量数据在系统盘。

## 📌 目标

不改动系统文件、不影响软件使用的前提下，将部分占用大的应用移到其他盘，并通过软链接（目录符号链接）指向原目录。

??? tip "软链接说明"

    | 类型 | 权限要求 | 跨硬盘 | 跨网络 | 相对路径 | 对软件透明性 | 典型场景 |
    |------|----------|--------|--------|----------|--------------|----------|
    | `mklink /J` (目录联接) | 普通用户（通常） | ✅ 本地卷 | ❌ | ❌ | ✅ 完全透明 | 迁移 `AppData\Local` 到同机其他盘 |
    | `mklink /D` (目录符号链接) | **管理员**（默认） | ✅ | ✅ (UNC) | ✅ | ✅ 完全透明 | 指向网络共享、跨硬盘迁移 |
    | `ln -s` (Linux) | 任意用户 | ✅ | ✅ | ✅ | ✅ 完全透明 | Linux 下所有软链接场景 |
    | 快捷方式 (.lnk) | 无特殊要求 | ✅ | ✅ | ✅ | ❌ 需Shell支持 | 只适合用户手动双击访问，不适于系统路径重定向 |

## 📌 步骤

### 🚁 1. 找“空间杀手”

- 下载 [WizTree](https://wiztreefree.com/)
- 扫描 C 盘，重点关注：
  ```
  C:\Users\你的用户名\AppData\Local
  C:\Users\你的用户名\AppData\Roaming
  ```
- 记下最占空间的**应用文件夹**（如 `JetBrains`、`Docker`、`Google`、`Microsoft`、`Trae CN` 等目录）

### 🚁 2. 针对单个应用目录迁移

复制并保存`Migrate-Folder.ps1`，管理员 PowerShell 中执行：

```powershell
.\Migrate-Folder.ps1 -SourceDir "C:\Users\你的用户名\AppData\Roaming\Trae CN" -TargetDir "G:\UserData\Trae CN"
```

若只想换盘符并保留原路径结构：

```powershell
.\Migrate-Folder.ps1 -SourceDir "C:\Users\你的用户名\AppData\Roaming\Trae CN" -TargetDir "G"
```

目标目录会自动将目标路径扩展为 `G:\Users\你的用户名\AppData\Roaming\Trae CN`

??? note "Migrate-Folder.ps1"

    ```powershell
    <#
    .SYNOPSIS
    将 Windows 下的任意文件夹迁移到其他位置，并创建符号链接。

    .DESCRIPTION
    脚本会并行复制目录（保留权限）→ 备份原目录 → 创建符号链接。
    支持自动将目标盘符扩展为完整路径（若只输入盘符）。
    支持自定义备份后缀和 robocopy 线程数。

    .PARAMETER SourceDir
    要迁移的原始目录（完整路径，如 C:\Users\name\AppData\Roaming\Trae CN）

    .PARAMETER TargetDir
    目标位置。可以是：
    - 完整目录路径（如 D:\Data\TraeCache）
    - 仅盘符（如 G 或 G:），此时自动保留源路径的相对结构
                        （例如源 C:\A\B，目标 G: → G:\A\B）

    .PARAMETER BackupSuffix
    备份文件夹的后缀，默认为 ".bak"

    .PARAMETER RoboThreads
    robocopy 并行线程数，默认 16（适合机械硬盘）

    .PARAMETER Help
    显示此帮助信息

    .EXAMPLE
    .\Migrate-Folder.ps1 -SourceDir "C:\Users\你的用户名\AppData\Roaming\Trae CN" -TargetDir "G:\TraeData"

    .EXAMPLE
    .\Migrate-Folder.ps1 -SourceDir "C:\Users\你的用户名\AppData\Roaming\Trae CN" -TargetDir "G"

    .EXAMPLE
    .\Migrate-Folder.ps1 -SourceDir "C:\ProgramData\Docker" -TargetDir "D:" -BackupSuffix "_old" -RoboThreads 8

    .EXAMPLE
    .\Migrate-Folder.ps1 -Help
    #>

    param(
        [Parameter(Mandatory=$false)]
        [string]$SourceDir,
        
        [Parameter(Mandatory=$false)]
        [string]$TargetDir,
        
        [Parameter(Mandatory=$false)]
        [string]$BackupSuffix = ".bak",
        
        [Parameter(Mandatory=$false)]
        [int]$RoboThreads = 16,
        
        [Parameter(Mandatory=$false)]
        [switch]$Help
    )

    # ---------- 显示帮助并退出 ----------
    if ($Help -or (-not $SourceDir) -or (-not $TargetDir)) {
        $helpText = @"
    ============================================
        目录迁移工具 - 帮助信息
    ============================================

    功能：
    将任意文件夹迁移到其他位置（跨硬盘），并用符号链接（Symbolic Link）指向新位置。
    复制过程保留 NTFS 权限、所有者和时间戳，使用多线程加速。

    用法：
    .\Migrate-Folder.ps1 -SourceDir <源路径> -TargetDir <目标路径> [选项]

    必选参数：
    -SourceDir      要迁移的原始目录（必须存在）
    -TargetDir      目标位置。可以是完整路径，或仅盘符（如 G:）
                    * 若只输入盘符，会自动保留源目录的相对路径结构。
                        例如：源 C:\Users\A\B，目标 G: → G:\Users\A\B

    可选参数：
    -BackupSuffix   原目录重命名的后缀，默认为 ".bak"
                    例如备份为 "Trae CN.bak"
    -RoboThreads    robocopy 并行线程数，默认 16
                    * 机械硬盘推荐 16，SSD 可降至 8 或 4
    -Help           显示此帮助信息

    示例：
    1. 迁移到自定义目录：
        .\Migrate-Folder.ps1 -SourceDir "C:\Users\你的用户名\AppData\Roaming\Trae CN" -TargetDir "G:\MyData\Trae"

    2. 只指定目标盘符（自动保持路径结构）：
        .\Migrate-Folder.ps1 -SourceDir "C:\Users\你的用户名\AppData\Roaming\Trae CN" -TargetDir "G"

    3. 自定义备份后缀和线程数：
        .\Migrate-Folder.ps1 -SourceDir "C:\ProgramData\Docker" -TargetDir "D:\DockerCache" -BackupSuffix "_backup" -RoboThreads 8

    4. 查看帮助：
        .\Migrate-Folder.ps1 -Help

    注意：
    * 必须以管理员身份运行 PowerShell。
    * 迁移过程中原目录会被重命名为“原名.backup”，软件若正在使用可能失败。
    * 迁移后请测试软件是否正常；若正常可手动删除备份目录。
    * 回滚方法见脚本执行后的提示。

    ============================================
    "@
        Write-Host $helpText -ForegroundColor Cyan
        if (-not $SourceDir -or -not $TargetDir) {
            Write-Host "错误：请提供 -SourceDir 和 -TargetDir 参数，或使用 -Help 查看帮助。" -ForegroundColor Red
        }
        exit 0
    }

    # ---------- 管理员权限检查 ----------
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-Host "错误：此脚本需要管理员权限才能创建符号链接。" -ForegroundColor Red
        Write-Host "请右键 PowerShell 图标 -> 以管理员身份运行。" -ForegroundColor Yellow
        exit 1
    }

    # ---------- 路径规范化 ----------
    $SourceDir = $SourceDir.TrimEnd('\')
    $TargetDir = $TargetDir.TrimEnd('\')

    # ---------- 智能处理 TargetDir：若为盘符则自动展开 ----------
    # 匹配盘符模式：单个字母后跟冒号（可选），如 "G" 或 "G:"
    if ($TargetDir -match '^[A-Za-z]:?$') {
        $drive = $TargetDir -replace ':$', ''  # 去除冒号，取字母
        $drive = $drive + ":"                  # 补回冒号，得到 "G:"
        
        # 提取源路径中盘符之后的部分（去掉开头的 "C:\" 或类似盘符）
        # 方法：取源路径的根路径之后的部分
        $relativePath = $SourceDir.Substring(3)  # 跳过前3个字符 "C:\"
        # 注意：如果源路径盘符长度可能不同（如 "D:\"），更通用的写法：
        # $relativePath = $SourceDir -replace '^[A-Za-z]:\\', ''
        # 但上面的简单写法假设源路径是 "C:\..." 形式，足够通用。
        # 为了避免盘符长度不同，改用正则：
        $relativePath = $SourceDir -replace '^[A-Za-z]:\\', ''
        $autoTarget = Join-Path -Path $drive -ChildPath $relativePath
        Write-Host "目标盘符已展开为完整路径：" -ForegroundColor Cyan
        Write-Host "  原始输入: $TargetDir" -ForegroundColor White
        Write-Host "  自动生成: $autoTarget" -ForegroundColor White
        $TargetDir = $autoTarget
    }

    # ---------- 其他变量 ----------
    $SourceParent = Split-Path $SourceDir -Parent
    $SourceLeaf = Split-Path $SourceDir -Leaf
    $BackupDir = Join-Path $SourceParent "$SourceLeaf$BackupSuffix"

    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "目录迁移工具 (保持符号链接)" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "源目录: $SourceDir" -ForegroundColor White
    Write-Host "目标目录: $TargetDir" -ForegroundColor White
    Write-Host "备份目录: $BackupDir" -ForegroundColor White
    Write-Host "并行线程: $RoboThreads" -ForegroundColor White
    Write-Host "============================================" -ForegroundColor Cyan

    # ---------- 检查源目录 ----------
    if (-not (Test-Path $SourceDir)) {
        Write-Host "错误：源目录不存在 -> $SourceDir" -ForegroundColor Red
        exit 1
    }

    # ---------- 检查目标盘符是否存在（如果 TargetDir 包含盘符） ----------
    $targetDrive = Split-Path -Qualifier $TargetDir
    if ($targetDrive -and -not (Test-Path $targetDrive)) {
        Write-Host "错误：目标盘符 $targetDrive 不存在或不可访问。" -ForegroundColor Red
        exit 1
    }

    # ---------- 确保目标父目录存在 ----------
    $TargetParent = Split-Path $TargetDir -Parent
    if ($TargetParent -and -not (Test-Path $TargetParent)) {
        Write-Host "正在创建目标父目录: $TargetParent" -ForegroundColor Yellow
        New-Item -Path $TargetParent -ItemType Directory -Force | Out-Null
    }

    # ---------- 复制（并行 robocopy） ----------
    Write-Host "正在复制文件（多线程 $RoboThreads）..." -ForegroundColor Yellow
    try {
        & robocopy.exe $SourceDir $TargetDir /E /COPYALL /DCOPY:T /R:2 /W:5 /MT:$RoboThreads /NP /NDL
        $exitCode = $LASTEXITCODE
        if ($exitCode -ge 8) {
            throw "robocopy 返回错误码 $exitCode"
        }
    } catch {
        Write-Host "复制失败：$_" -ForegroundColor Red
        Write-Host "请检查目标磁盘空间、权限，或尝试更小的线程数（如 /MT:8）。" -ForegroundColor Yellow
        exit 1
    }

    # ---------- 备份原目录 ----------
    Write-Host "正在备份原目录: $BackupDir" -ForegroundColor Yellow
    try {
        Rename-Item -Path $SourceDir -NewName "$SourceLeaf$BackupSuffix" -ErrorAction Stop
    } catch {
        Write-Host "重命名失败，请确保没有程序正在使用该目录。错误：$_" -ForegroundColor Red
        Write-Host "你可以手动关闭相关软件后，将目标目录重命名为原名称。" -ForegroundColor Yellow
        exit 1
    }

    # ---------- 创建符号链接 ----------
    Write-Host "正在创建符号链接: $SourceDir -> $TargetDir" -ForegroundColor Yellow
    try {
        New-Item -Path $SourceDir -ItemType SymbolicLink -Target $TargetDir -Force -ErrorAction Stop | Out-Null
    } catch {
        Write-Host "创建符号链接失败，尝试恢复备份..." -ForegroundColor Red
        if (Test-Path $SourceDir) { Remove-Item $SourceDir -Force -ErrorAction SilentlyContinue }
        Rename-Item -Path $BackupDir -NewName $SourceLeaf -ErrorAction SilentlyContinue
        Write-Host "已恢复原目录。错误信息：$_" -ForegroundColor Red
        exit 1
    }

    Write-Host "============================================" -ForegroundColor Green
    Write-Host "迁移成功！" -ForegroundColor Green
    Write-Host "原目录已备份为：$BackupDir" -ForegroundColor Green
    Write-Host "符号链接已创建：$SourceDir -> $TargetDir" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "请测试软件是否正常工作。" -ForegroundColor Yellow
    Write-Host "如果一切正常，可手动删除备份目录：$BackupDir" -ForegroundColor Yellow
    Write-Host "若需回滚，请按以下步骤：" -ForegroundColor Yellow
    Write-Host "  1. 删除符号链接: Remove-Item '$SourceDir'" -ForegroundColor White
    Write-Host "  2. 恢复备份目录: Rename-Item '$BackupDir' '$SourceLeaf'" -ForegroundColor White
    ```

#### 脚本内容简述

| 步骤 | 操作 | 核心技术/命令 |
|------|------|----------------|
| 1 | 并行复制（保留权限、时间戳、所有者） | `robocopy /E /COPYALL /DCOPY:T /MT:16` |
| 2 | 原目录重命名为备份 | `Rename-Item`（原子操作，避免数据丢失） |
| 3 | 在原位置创建符号链接 | `New-Item -ItemType SymbolicLink -Target $TargetDir` |
| 4 | 失败自动回滚 | 删除残留链接，恢复备份目录名 |

> **作用原理**：利用 Windows 文件系统重解析点（Reparse Point），将原路径透明地重定向到新位置。应用读写 `C:\Users\...\AppData\...` 时，内核自动转向 G 盘，无需修改任何配置或代码。

#### 注意事项

- **务必以管理员身份运行 PowerShell**（创建符号链接需要权限）。
- 迁移前关闭目标应用（避免文件被锁定）。
- 机械硬盘作为目标盘时，**首次读写可能变慢**（尤其是大量小文件场景），建议只迁移不常用的大体积存档目录；频繁访问的缓存目录留在 SSD 。
- 如果软件在 C 盘重新创建了同名目录（不遵循符号链接），请改用 `mklink /J`（目录联接），或查阅软件文档修改数据目录路径。


### 🚁 3.验证与清理

- 启动原应用，检查功能正常。
- 确认数据已写入目标盘。
- 删除备份目录（原目录被自动重命名为 `原名.bak`）。


### 🚁 4.回滚（如果需要恢复）

```powershell
Remove-Item "C:\Users\你的用户名\AppData\Roaming\Trae CN"
Rename-Item "C:\Users\你的用户名\AppData\Roaming\Trae CN.bak" "Trae CN"
```
