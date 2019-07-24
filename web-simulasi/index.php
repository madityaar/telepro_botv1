<?php
// Create database connection using config file
include_once("config.php");

// Fetch all users data from database
$result = mysqli_query($mysqli, "SELECT * FROM mytable ORDER BY ODP DESC");
?>

<html>

<head>
    <title>Homepage</title>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">

    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

    <!-- Popper JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</head>

<body>
    <table class="table">
        <thead class="thead-dark">
            <tr>
                <th scope="col">ODP</th>
                <th scope="col">No Tiket</th>
                <th scope="col">Foto Sebelum</th>
                <th scope="col">Foto Progres</th>
                <th scope="col">Foto Sesudah</th>
                <th scope="col">Longitude ODP</th>
                <th scope="col">Latitude ODP </th>
                <th scope="col">Longitude Teknisi</th>
                <th scope="col">Latitude Teknisi</th>
                <th scope="col">Jarak</th>
                <th scope="col">Updated By</th>
                <th scope="col">Updated Date</th>
                <th scope="col">Keterangan</th>
            </tr>
        </thead>
        <?php
        while ($user_data = mysqli_fetch_array($result)) {
            echo "<tbody>";
            echo "<tr>";
            echo "<td>" . $user_data['ODP'] . "</td>";
            echo "<td>" . $user_data['TICKET_ID'] . "</td>";
            echo "<td>" . $user_data['PHOTO_BEFORE'] . "</td>";
            echo "<td>" . $user_data['PHOTO_PROCESS'] . "</td>";
            echo "<td>" . $user_data['PHOTO_AFTER'] . "</td>";
            echo "<td>" . $user_data['LONGITUDE'] . "</td>";
            echo "<td>" . $user_data['LATITUDE'] . "</td>";
            echo "<td>" . $user_data['LONGITUDE_U'] . "</td>";
            echo "<td>" . $user_data['LATITUDE_U'] . "</td>";
            echo "<td>" . $user_data['DISTANCE'] . "</td>";
            echo "<td>" . $user_data['UPDATED_BY'] . "</td>";
            echo "<td>" . $user_data['UPDATED_DATE'] . "</td>";
            echo "<td>" . $user_data['KETERANGAN'] . "</td>";
        }
        ?>
    </table>
</body>

</html>