-- Include full path (with trailing /)
DOMAIN = "http://blf02.net:8000/out"
IMAGE_DIRECTORY = "/video/"
IMAGE_MIN = 1
IMAGE_MAX = 24

-- DO NOT EDIT BELOW THIS LINE


-- Refresh directory
if fs.isDir(IMAGE_DIRECTORY) then
    fs.delete(IMAGE_DIRECTORY)
end
fs.makeDir(IMAGE_DIRECTORY)


-- Iterate through all image numbers
i = IMAGE_MIN
while i <= IMAGE_MAX do
    -- Leading 0's
    i_str = ""
    if i < 10 then
        i_str = "000" .. i
    elseif i < 100 then
        i_str = "00" .. i
    elseif i < 1000 then
        i_str = "0" .. i
    else
        i_str = "" .. i
    end
    -- wget the file (HTTP API may not be available!)
    shell.run("wget", DOMAIN .. i_str .. ".nfp", IMAGE_DIRECTORY .. i_str .. ".nfp")
    i = i + 1
end
