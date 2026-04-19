local HttpService = game:GetService("HttpService")

local API = "https://robloxscripthub-kfz9.onrender.com/validate"

-- must be passed or rechecked
local key = getgenv().script_key

if not key then
    return print("No key provided")
end

local res = request({
    Url = API,
    Method = "POST",
    Headers = {["Content-Type"] = "application/json"},
    Body = HttpService:JSONEncode({
        key = key,
        userId = game.Players.LocalPlayer.UserId
    })
})

local data = HttpService:JSONDecode(res.Body)

if not data.valid then
    return print("Blocked (invalid session)")
end

-- REAL SCRIPT STARTS HERE
print("Main script loaded")
