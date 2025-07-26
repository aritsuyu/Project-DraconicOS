#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <psapi.h>
#include <winternl.h>

#pragma comment(lib, "ntdll.lib")
#pragma comment(lib, "psapi.lib")

// Definições para APIs não documentadas
typedef enum _SYSTEM_INFORMATION_CLASS {
    SystemBasicInformation = 0,
    SystemMemoryListInformation = 80
} SYSTEM_INFORMATION_CLASS;

typedef enum _SYSTEM_MEMORY_LIST_COMMAND {
    MemoryCaptureAccessedBits,
    MemoryCaptureAndResetAccessedBits,
    MemoryEmptyWorkingSets,           // Limpa working sets
    MemoryFlushModifiedList,          // Flush modified pages
    MemoryPurgeStandbyList,           // Limpa standby list
    MemoryPurgeLowPriorityStandbyList,// Limpa standby de baixa prioridade
    MemoryCommandMax
} SYSTEM_MEMORY_LIST_COMMAND;

// Função não documentada do ntdll.dll
typedef NTSTATUS (WINAPI *pNtSetSystemInformation)(
    SYSTEM_INFORMATION_CLASS SystemInformationClass,
    PVOID SystemInformation,
    ULONG SystemInformationLength
);

// Estrutura para informações de memória
typedef struct {
    DWORDLONG totalPhys;
    DWORDLONG availPhys;
    DWORDLONG usedPhys;
    DWORD memoryLoad;
} MEMORY_INFO;

// Cores para console
#define COLOR_RED     12
#define COLOR_GREEN   10
#define COLOR_YELLOW  14
#define COLOR_CYAN    11
#define COLOR_WHITE   15
#define COLOR_GRAY    8

void setConsoleColor(int color) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}

void resetConsoleColor() {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), COLOR_WHITE);
}

BOOL isAdmin() {
    BOOL isAdmin = FALSE;
    PSID adminGroup = NULL;
    SID_IDENTIFIER_AUTHORITY ntAuthority = SECURITY_NT_AUTHORITY;
    
    if (AllocateAndInitializeSid(&ntAuthority, 2, SECURITY_BUILTIN_DOMAIN_RID,
                                DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0, &adminGroup)) {
        CheckTokenMembership(NULL, adminGroup, &isAdmin);
        FreeSid(adminGroup);
    }
    return isAdmin;
}

BOOL enableDebugPrivilege() {
    HANDLE hToken;
    TOKEN_PRIVILEGES tp;
    LUID luid;
    
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken)) {
        return FALSE;
    }
    
    if (!LookupPrivilegeValue(NULL, SE_DEBUG_NAME, &luid)) {
        CloseHandle(hToken);
        return FALSE;
    }
    
    tp.PrivilegeCount = 1;
    tp.Privileges[0].Luid = luid;
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    
    BOOL result = AdjustTokenPrivileges(hToken, FALSE, &tp, sizeof(TOKEN_PRIVILEGES), NULL, NULL);
    CloseHandle(hToken);
    return result;
}

BOOL getMemoryInfo(MEMORY_INFO* memInfo) {
    MEMORYSTATUSEX memStatus;
    memStatus.dwLength = sizeof(MEMORYSTATUSEX);
    
    if (!GlobalMemoryStatusEx(&memStatus)) {
        return FALSE;
    }
    
    memInfo->totalPhys = memStatus.ullTotalPhys;
    memInfo->availPhys = memStatus.ullAvailPhys;
    memInfo->usedPhys = memStatus.ullTotalPhys - memStatus.ullAvailPhys;
    memInfo->memoryLoad = memStatus.dwMemoryLoad;
    
    return TRUE;
}

void formatBytes(DWORDLONG bytes, char* buffer, size_t bufferSize) {
    const char* units[] = {"B", "KB", "MB", "GB", "TB"};
    int unitIndex = 0;
    double size = (double)bytes;
    
    while (size >= 1024.0 && unitIndex < 4) {
        size /= 1024.0;
        unitIndex++;
    }
    
    snprintf(buffer, bufferSize, "%.1f %s", size, units[unitIndex]);
}

void printMemoryStatus(MEMORY_INFO* memInfo) {
    char totalStr[32], usedStr[32], availStr[32];
    formatBytes(memInfo->totalPhys, totalStr, sizeof(totalStr));
    formatBytes(memInfo->usedPhys, usedStr, sizeof(usedStr));
    formatBytes(memInfo->availPhys, availStr, sizeof(availStr));
    
    printf("\n");
    setConsoleColor(COLOR_CYAN);
    printf("=== MEMORY STATUS ===\n");
    resetConsoleColor();
    
    printf("Total Memory:     %s\n", totalStr);
    printf("Used Memory:      %s (%d%%)\n", usedStr, memInfo->memoryLoad);
    printf("Available Memory: %s\n", availStr);
    
    // Barra de uso da memória
    printf("Usage: [");
    int barLength = 30;
    int usedLength = (memInfo->memoryLoad * barLength) / 100;
    
    if (memInfo->memoryLoad > 85) setConsoleColor(COLOR_RED);
    else if (memInfo->memoryLoad > 70) setConsoleColor(COLOR_YELLOW);
    else setConsoleColor(COLOR_GREEN);
    
    for (int i = 0; i < barLength; i++) {
        if (i < usedLength) printf("█");
        else printf("░");
    }
    printf("] %d%%", memInfo->memoryLoad);
    resetConsoleColor();
    
    if (memInfo->memoryLoad > 85) {
        setConsoleColor(COLOR_RED);
        printf(" CRITICAL");
    } else if (memInfo->memoryLoad > 70) {
        setConsoleColor(COLOR_YELLOW);
        printf(" HIGH");
    } else {
        setConsoleColor(COLOR_GREEN);
        printf(" NORMAL");
    }
    resetConsoleColor();
    printf("\n");
}

BOOL clearWorkingSets() {
    printf("Clearing working sets... ");
    
    // Limpar working set do processo atual
    if (!SetProcessWorkingSetSize(GetCurrentProcess(), (SIZE_T)-1, (SIZE_T)-1)) {
        setConsoleColor(COLOR_RED);
        printf("FAILED\n");
        resetConsoleColor();
        return FALSE;
    }
    
    // Tentar limpar working sets de todos os processos
    DWORD processes[1024], needed, processCount;
    if (EnumProcesses(processes, sizeof(processes), &needed)) {
        processCount = needed / sizeof(DWORD);
        int cleared = 0;
        
        for (DWORD i = 0; i < processCount; i++) {
            HANDLE hProcess = OpenProcess(PROCESS_SET_QUOTA, FALSE, processes[i]);
            if (hProcess) {
                if (SetProcessWorkingSetSize(hProcess, (SIZE_T)-1, (SIZE_T)-1)) {
                    cleared++;
                }
                CloseHandle(hProcess);
            }
        }
        
        setConsoleColor(COLOR_GREEN);
        printf("OK (%d processes)\n", cleared);
        resetConsoleColor();
        return TRUE;
    }
    
    setConsoleColor(COLOR_YELLOW);
    printf("PARTIAL\n");
    resetConsoleColor();
    return TRUE;
}

BOOL clearStandbyMemory() {
    printf("Clearing standby memory... ");
    
    HMODULE hNtdll = GetModuleHandle(L"ntdll.dll");
    if (!hNtdll) {
        setConsoleColor(COLOR_RED);
        printf("FAILED (ntdll not found)\n");
        resetConsoleColor();
        return FALSE;
    }
    
    pNtSetSystemInformation NtSetSystemInformation = 
        (pNtSetSystemInformation)GetProcAddress(hNtdll, "NtSetSystemInformation");
    
    if (!NtSetSystemInformation) {
        setConsoleColor(COLOR_RED);
        printf("FAILED (API not found)\n");
        resetConsoleColor();
        return FALSE;
    }
    
    // Limpar different types of standby memory
    SYSTEM_MEMORY_LIST_COMMAND commands[] = {
        MemoryPurgeStandbyList,
        MemoryPurgeLowPriorityStandbyList,
        MemoryFlushModifiedList
    };
    
    int success = 0;
    for (int i = 0; i < 3; i++) {
        NTSTATUS status = NtSetSystemInformation(SystemMemoryListInformation, 
                                               &commands[i], sizeof(commands[i]));
        if (NT_SUCCESS(status)) {
            success++;
        }
    }
    
    if (success > 0) {
        setConsoleColor(COLOR_GREEN);
        printf("OK (%d/3 operations)\n", success);
        resetConsoleColor();
        return TRUE;
    } else {
        setConsoleColor(COLOR_RED);
        printf("FAILED\n");
        resetConsoleColor();
        return FALSE;
    }
}

BOOL clearModifiedPageList() {
    printf("Clearing modified page list... ");
    
    HMODULE hNtdll = GetModuleHandle(L"ntdll.dll");
    if (!hNtdll) {
        setConsoleColor(COLOR_RED);
        printf("FAILED\n");
        resetConsoleColor();
        return FALSE;
    }
    
    pNtSetSystemInformation NtSetSystemInformation = 
        (pNtSetSystemInformation)GetProcAddress(hNtdll, "NtSetSystemInformation");
    
    if (!NtSetSystemInformation) {
        setConsoleColor(COLOR_RED);
        printf("FAILED\n");
        resetConsoleColor();
        return FALSE;
    }
    
    SYSTEM_MEMORY_LIST_COMMAND command = MemoryFlushModifiedList;
    NTSTATUS status = NtSetSystemInformation(SystemMemoryListInformation, 
                                           &command, sizeof(command));
    
    if (NT_SUCCESS(status)) {
        setConsoleColor(COLOR_GREEN);
        printf("OK\n");
        resetConsoleColor();
        return TRUE;
    } else {
        setConsoleColor(COLOR_RED);
        printf("FAILED\n");
        resetConsoleColor();
        return FALSE;
    }
}

void clearAllMemory() {
    MEMORY_INFO beforeMem, afterMem;
    
    printf("\n");
    setConsoleColor(COLOR_CYAN);
    printf("=== MEMORY CLEANUP STARTED ===\n");
    resetConsoleColor();
    
    if (!getMemoryInfo(&beforeMem)) {
        setConsoleColor(COLOR_RED);
        printf("Error: Could not get memory information\n");
        resetConsoleColor();
        return;
    }
    
    printf("Memory usage before: %d%%\n\n", beforeMem.memoryLoad);
    
    // Executar limpezas
    clearWorkingSets();
    Sleep(500);  // Pequena pausa entre operações
    
    clearModifiedPageList();
    Sleep(500);
    
    clearStandbyMemory();
    Sleep(1000);  // Esperar sistema atualizar
    
    // Verificar resultado
    if (getMemoryInfo(&afterMem)) {
        printf("\n");
        setConsoleColor(COLOR_CYAN);
        printf("=== CLEANUP RESULTS ===\n");
        resetConsoleColor();
        
        printf("Memory usage after:  %d%%\n", afterMem.memoryLoad);
        
        DWORDLONG freed = beforeMem.usedPhys - afterMem.usedPhys;
        if (freed > 0) {
            char freedStr[32];
            formatBytes(freed, freedStr, sizeof(freedStr));
            setConsoleColor(COLOR_GREEN);
            printf("Memory freed: %s\n", freedStr);
            resetConsoleColor();
        } else {
            setConsoleColor(COLOR_YELLOW);
            printf("No significant memory freed\n");
            resetConsoleColor();
        }
        
        printMemoryStatus(&afterMem);
    }
}

void printUsage() {
    printf("Windows Memory Cleaner - C Version\n");
    printf("Usage:\n");
    printf("  memclean.exe                 - Show memory status\n");
    printf("  memclean.exe -c              - Clean all memory\n");
    printf("  memclean.exe -w              - Clean working sets only\n");
    printf("  memclean.exe -s              - Clean standby memory only\n");
    printf("  memclean.exe -m              - Clean modified pages only\n");
    printf("  memclean.exe -h              - Show this help\n");
}

int main(int argc, char** argv) {
    // Configurar console
    SetConsoleOutputCP(CP_UTF8);
    
    setConsoleColor(COLOR_CYAN);
    printf("========================================\n");
    printf("  WINDOWS MEMORY CLEANER - C VERSION\n");
    printf("  High-performance memory management\n");
    printf("========================================\n");
    resetConsoleColor();
    
    printf("System: Windows\n");
    printf("Administrator: %s\n", isAdmin() ? "YES" : "NO");
    
    if (!isAdmin()) {
        setConsoleColor(COLOR_RED);
        printf("WARNING: Not running as Administrator!\n");
        printf("Memory cleaning will be limited.\n");
        resetConsoleColor();
    } else {
        enableDebugPrivilege();
    }
    
    // Processar argumentos
    if (argc == 1) {
        // Mostrar status da memória
        MEMORY_INFO memInfo;
        if (getMemoryInfo(&memInfo)) {
            printMemoryStatus(&memInfo);
        }
    } else if (argc == 2) {
        if (strcmp(argv[1], "-c") == 0) {
            clearAllMemory();
        } else if (strcmp(argv[1], "-w") == 0) {
            printf("\n");
            clearWorkingSets();
        } else if (strcmp(argv[1], "-s") == 0) {
            printf("\n");
            clearStandbyMemory();
        } else if (strcmp(argv[1], "-m") == 0) {
            printf("\n");
            clearModifiedPageList();
        } else if (strcmp(argv[1], "-h") == 0) {
            printUsage();
        } else {
            printf("Invalid argument. Use -h for help.\n");
        }
    } else {
        printUsage();
    }
    
    printf("\n========================================\n");
    return 0;
}