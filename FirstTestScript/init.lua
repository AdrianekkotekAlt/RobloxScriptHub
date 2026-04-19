local HttpService = game:GetService("HttpService")

local API = "https://robloxscripthub-kfz9.onrender.com/validate"

local key = "USER_INPUT_KEY"

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

if data.valid then
    print("Key valid")

    -- load main script ONLY after validation
    loadstring(game:HttpGet("https://raw.githubusercontent.com/.../main.lua"))()
else
    print("Invalid key")
end
