-- Include trailing /
IMAGE_DIRECTORY = "/video/"
MONITOR_SIDE = "left"
-- DO NOT EDIT BELOW THIS LINE


-- Set text size for monitor
monitor = peripheral.wrap(MONITOR_SIDE)
monitor.setTextScale(0.5)



-- Check that IMAGE_DIRECTORY exists --
if not fs.isDir(IMAGE_DIRECTORY) then
    error(IMAGE_DIRECTORY + " does not exist!")
end

-- Get all files and start with first one
files = fs.list(IMAGE_DIRECTORY)
file = files[1]
i = 1
while file ~= nil do
    -- Load and draw image before getting next one ready
    image = paintutils.loadImage(IMAGE_DIRECTORY .. file)
    paintutils.drawImage(image, 1, 1)
    i = i + 1
    file = files[i]
    sleep(0.10)
end
