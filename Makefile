# Makefile

# Define variables
VIDEO_FILE = videos.txt
PYTHON_SCRIPT = video_to_gif.py
PROCESSED_FILE = processed_videos.txt

# Targets
all: gifs

# Rule to generate GIFs
gifs: $(VIDEO_FILE) $(PROCESSED_FILE)
	@echo "Running video_to_gif.py to process videos..."
	python $(PYTHON_SCRIPT)

# Check if processed_videos.txt is out of date
$(PROCESSED_FILE): $(VIDEO_FILE)
	@# Ensure the processed_videos.txt exists
	@if [ ! -f $(PROCESSED_FILE) ]; then touch $(PROCESSED_FILE); fi

# Phony targets
.PHONY: all gifs
