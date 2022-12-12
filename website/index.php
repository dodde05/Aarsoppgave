<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="style.css">
        <title>Leaderboard</title>
    </head>
    <body>
        <h1>Leaderboards</h1>

        <table>

            <tr>
                <th>Rank</th>
                <th>Name</th>
                <th>Score</th>
                <th>Date</th>
            </tr>
            <?php

                $host = "localhost";
                $user = "client";
                $password = "79E76w864dcKbja";
                $database = "highscores";

                $connect = mysqli_connect($host, $user, $password, $database);

                $sql = "SELECT id, name, score, DATE_FORMAT(date, '%d.%m.%Y') date FROM attempt ORDER BY score DESC;";

                $result = mysqli_query($connect, $sql);
                $numberOfResults = mysqli_num_rows($result);

                if ($numberOfResults > 0) {
                    $rank = 1;
                    while($row = mysqli_fetch_assoc($result)){
                        echo "<tr>" .
                        "<td>" . $rank . "." . "</td>" .
                        "<td>" . $row["name"] . "</td>" .
                        "<td>" . $row["score"] . "</td>" .
                        "<td>" . $row["date"] . "</td>" .
                        "</tr>";
                        $rank++;
                    }
                }

            ?>

        </table>

    </body>
</html>