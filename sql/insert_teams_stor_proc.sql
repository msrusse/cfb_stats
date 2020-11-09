CREATE PROC insertTeam(@ID as INT, @name as VARCHAR(max), @conference as VARCHAR(50))
AS
BEGIN
    INSERT INTO dbo.teams (
        [ID], 
        [name], 
        [conference]
    )
    VALUES (
        @ID,
        @name,
        @conference
    )
END;