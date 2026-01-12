import asyncio
from app.video.models import Video
from pathlib import Path
import tempfile
from app.common.utils import download_file_remote_to_local, get_url_from_s3_key
import logging
logger = logging.getLogger(__name__)

async def compile_video(video: Video, output_dir: str):
    logger.info(f"Compiling video {video.id} with {len(video.scenes)} scenes")
    try:
        temp_dir = Path(tempfile.mkdtemp())
        
        sorted_scenes = sorted(video.scenes, key=lambda x: x.order_number)
        scene_files = []
        for i, scene in enumerate(sorted_scenes):
            scene_data = {
                "image": None, 
                "audio": None,
                "duration": scene.duration_seconds,
                "order_number": scene.order_number
            }
            
            if scene.image_file_key:
                image_url = get_url_from_s3_key(scene.image_file_key)
                image_path = temp_dir / f"scene_image_{scene.order_number}.jpg"
                await download_file_remote_to_local(image_url, image_path)
                scene_data['image'] = str(image_path)
                
            audio_path = temp_dir / f"scene_audio_{scene.order_number}.mp3"
            await download_file_remote_to_local(scene.audio_url, audio_path)
            scene_data['audio'] = str(audio_path)
                
            scene_files.append(scene_data)
        
        video_clips = []
        for i, scene_data in enumerate(scene_files):
            
            clip_path = temp_dir / f"clip_{i}.mp4"
            if scene_data['image']:
                #create a video from image with audio
                cmd = [
                    'ffmpeg',
                    '-loop', '1',
                    '-i', scene_data["image"],
                    '-i', scene_data["audio"],
                    '-c:v', 'libx264',
                    '-tune', 'stillimage',
                    '-c:a', 'aac',
                    '-b:a', '192k',
                    '-pix_fmt', 'yuv420p',
                    '-shortest',
                    '-vf', f'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1',
                    '-t', str(scene_data["duration"]),
                    '-y',
                    str(clip_path)
                ]
            else:
                #crate a black video with audio for scenes without images
                cmd = [
                    'ffmpeg',
                    '-f', 'lavfi',
                    '-i', 'color=c=black:s=1920x1080:d=' + str(scene_data["duration"]),
                    '-i', scene_data["audio"],
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-b:a', '192k',
                    '-pix_fmt', 'yuv420p',
                    '-shortest',
                    '-y',
                    str(clip_path)
                ]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"FFmpeg process failed for clip {i} pm video {video.id} with return code {process.returncode}")
            video_clips.append(str(clip_path))
    
        concat_file = temp_dir / "concat.txt"
        with open(concat_file, "w") as f:
            for clip in video_clips:
                f.write(f"file '{clip}'\n")
                
        #merge all clips
        output_path = Path(output_dir) / f"{video.id}.mp4"
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            '-y',
            str(output_path)
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"FFmpeg process failed for merging clips for video {video.id} with return code {process.returncode}")\
                
        import shutil
        shutil.rmtree(temp_dir)
        return str(output_path)
    
    
    except Exception as e:
        logger.error(f"Error compiling video: {e}")
        pass