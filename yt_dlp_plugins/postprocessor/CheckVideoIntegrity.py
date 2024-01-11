# ⚠ Don't use relative imports
from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp.postprocessor import FFmpegPostProcessor
from yt_dlp.utils import (
    encodeArgument,
    encodeFilename,
    Popen,
    shell_quote,
)
import subprocess
import os
import platform

# ℹ️ See the docstring of yt_dlp.postprocessor.common.PostProcessor

# ⚠ The class name must end in "PP"


class CheckVideoIntegrityPP(FFmpegPostProcessor):
    def __init__(self, downloader=None, **kwargs):
        # ⚠ Only kwargs can be passed from the CLI, and all argument values will be string
        # Also, "downloader", "when" and "key" are reserved names
        super().__init__(downloader)
        self._kwargs = kwargs
        
    # run the supplied command to get duration and compare it with the metadata
    def checkLength(self, cmd, desc, duration):
        stdout, _, _ = Popen.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        if not stdout:
            raise Exception('Could not extract ' + desc + '.')
        if self._duration_mismatch(float(stdout), duration, 1):
            raise Exception('Duration mismatch in ' + desc + '.')
        self.to_screen(desc[0:1].upper() + desc[1:] + ' OK.') #Upper is not defined

    # ℹ️ See docstring of yt_dlp.postprocessor.common.PostProcessor.run
    def run(self, info):
        filepath = info.get('filepath')
        if filepath:  # Video is downloaded; continue
            # check different bits of length info to look for issues during download
            self.to_screen('Checking video duration info...')
            duration = info.get('duration')
            if platform.system() == 'Windows':
                cmd = 'Powershell.exe -executionpolicy remotesigned -File "' + os.path.dirname(__file__) + '\getfilelengthmetadata.ps1" "' + os.path.abspath(filepath) + '"'
                self.checkLength(cmd, 'file duration metadata', duration)
            else:
                self.to_screen('This plugin does not yet support getting file metadata on your platform. Pull requests are welcome.')
            if self._duration_mismatch(self._get_real_video_duration(info['filepath']), duration, 1):
                raise Exception('Duration mismatch in video file length.')
            self.to_screen('Video file length OK.')
            cmd = encodeFilename(self.probe_executable, True) + ' -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "'+ self._ffmpeg_filename_argument(filepath) + '"'
            self.checkLength(cmd, 'video container length', duration)
            cmd = encodeFilename(self.probe_executable, True) + ' -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 "' + self._ffmpeg_filename_argument(filepath) + '"'
            self.checkLength(cmd, 'video stream length', duration)
            cmd = encodeFilename(self.probe_executable, True) + ' -v error -select_streams a:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 "' + self._ffmpeg_filename_argument(filepath) + '"'
            self.checkLength(cmd, 'audio stream length', duration)
            self.to_screen('Video duration info matches site metadata.')
            
            #check video file integrity
            self.to_screen('Checking video integrity...')
            cmd = encodeFilename(self.executable, True) +  ' -v error -i "' + self._ffmpeg_filename_argument(filepath) + '" -f null - -xerror'
            subprocess.check_call(cmd)
            self.to_screen('No issues detected.')
            
        else:  # PP was called before actual download which is pointless, so just error out
            raise Exception("This postprocessor is useless if called before the download")
        return [], info  # return list_of_files_to_delete, info_dict
