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
    // Fetch the next satellite pass
    const fetchNextPass = async () => {
      try {
        const response = await axios.get(
          "http://" + window.location.hostname + ":8000/dashboard/next-pass"
        ); // Adjust the API endpoint
        setNextPass(response.data);
        updateCountdown(response.data.aos); // 'aos' is the datetime of Acquisition of Signal
      } catch (error) {
        console.error("Error fetching satellite pass data:", error);
      }
    };

    fetchNextPass();
  }, []);

  useEffect(() => {
    // Update countdown every second
    const interval = setInterval(() => {
      if (nextPass) {
        updateCountdown(nextPass.aos);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [nextPass]);

  // Function to update the countdown
  const updateCountdown = (aosTime) => {
    const aos = new Date(aosTime);
    const now = new Date();
    const timeLeft = aos - now;

    if (timeLeft > 0) {
      const hours = Math.floor((timeLeft / (1000 * 60 * 60)) % 24);
      const minutes = Math.floor((timeLeft / 1000 / 60) % 60);
      const seconds = Math.floor((timeLeft / 1000) % 60);
      setCountdown(`${hours}h ${minutes}m ${seconds}s`);
    } else {
      setCountdown("Pass is currently happening or has finished.");
    }
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={6}>
          <Grid item xs={12}>
            <Card>
              <MDBox p={3}>
                <h2>Next Satellite Pass Countdown:</h2>
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
