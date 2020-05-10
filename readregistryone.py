import errno
import os
import winreg


def architecture(arch_term):
    if arch_term in os.environ:
        return os.environ[arch_term].lower()
    else:
        return False


system32 = architecture('PROCESSOR_ARCHITECTURE')
system64 = architecture('PROCESSOR_ARCHITEW6432')

if system32 == 'x86' and not system64:
    registryElements = {0}  # if system architecture is only 32 bits
elif system32 == 'amd64':
    registryElements = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}  # if system architecture is 64 bits
    """This approach will ensure that the registry access, no matter if it's a 32 or 64 bit process, 
    will access the 64 bit registry view (KEY_WOW64_64KEY) and he registry access, no matter if it's a 32 or 64 bit process, 
    will access the 32 bit registry view (KEY_WOW64_32KEY)."""
else:
    raise Exception("Can't process architecture type: {}".format(system32))

for element in registryElements:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0,
                         winreg.KEY_READ | element)
    for i in range(0, winreg.QueryInfoKey(key)[0]):
        elementName = winreg.EnumKey(key, i)
        registryKey = winreg.OpenKey(key, elementName)
        try:
            print(winreg.QueryValueEx(registryKey, 'DisplayName')[0])
        except OSError as e:
            if e.errno == errno.ENOENT:
                print("DisplayName element does not exist for the Registry sub key name: {}". format(elementName))
                pass
        finally:
            registryKey.Close()
