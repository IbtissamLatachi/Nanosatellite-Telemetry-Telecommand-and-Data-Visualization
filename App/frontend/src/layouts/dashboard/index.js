import { useState, useEffect } from "react";
import axios from "axios";

// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";

function Dashboard() {
  const [nextPass, setNextPass] = useState(null);
  const [countdown, setCountdown] = useState("");

  useEffect(() => {
    // Function to fetch the next satellite pass
    const fetchNextPass = async () => {
      try {
        const response = await axios.get(
          "http://" + window.location.hostname + ":8000/dashboard/next-pass"
        );
        setNextPass(response.data);
      } catch (error) {
        console.error("Error fetching satellite pass data:", error);
      }
    };

    // Fetch the next satellite pass initially and after every pass ends
    fetchNextPass();
    const interval = setInterval(() => {
      fetchNextPass();
    }, 1000 * 60); // Check for the next pass every minute

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Update countdown every second
    const interval = setInterval(() => {
      if (nextPass) {
        updateCountdown(nextPass.aos, nextPass.los);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [nextPass]);

  // Function to update the countdown
  const updateCountdown = (aosTime, losTime) => {
    const aos = new Date(aosTime);
    const los = new Date(losTime);
    const now = new Date();

    if (now < aos) {
      // Before the pass starts
      setCountdown("Next pass in: " + formatTime(aos - now));
    } else if (now <= los) {
      // During the pass
      setCountdown(
        "Pass in progress. Time until LOS: " + formatTime(los - now)
      );
    } else {
      // After the pass ends
      setCountdown("Waiting for the next pass...");
    }
  };

  // Helper function to format time
  const formatTime = (milliseconds) => {
    const hours = Math.floor((milliseconds / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((milliseconds / 1000 / 60) % 60);
    const seconds = Math.floor((milliseconds / 1000) % 60);
    return `${hours}h ${minutes}m ${seconds}s`;
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={6}>
          <Grid item xs={12}>
            <Card>
              <MDBox p={3}>
                <h2>Satellite Pass Countdown:</h2>
                <p>{countdown}</p>
              </MDBox>
            </Card>
          </Grid>
        </Grid>
      </MDBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Dashboard;
