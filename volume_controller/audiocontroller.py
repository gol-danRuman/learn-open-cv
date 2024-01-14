

def set_volume(volume):
    """
    For Ubuntu OS
    :param volume:
    :return:
    """
    import alsaaudio
    mixer = alsaaudio.Mixer()
    mixer.setvolume(volume)

def volume_for_windows(volume):
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.GetMute()
    volume.GetMasterVolumeLevel()
    print(volume.GetVolumeRange())
    volume.SetMasterVolumeLevel(-20.0, None)


# Example: Set volume to 50%
set_volume(100)