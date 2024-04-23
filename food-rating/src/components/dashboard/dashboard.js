import './dashboard.css';

function Banner() {
    return (
        <div className="banner">
            <h1>Food Rating</h1>
        </div>
    );
}

function TopFoodItems() {
    return (
        <div>
            <h1>Top Food Items</h1>
        </div>
    );
}

function TopCompanies() {
    return (
        <div>
            <h1>Top Companies</h1>
        </div>
    );
}

function FoodEntries() {
    return (
        <div>
            <h1>Food Entries</h1>
        </div>
    );
}

function AddEntry() {
    return (
        <div>
            <h1>Add Entry</h1>
        </div>
    );
}

function Logout() {
    return (
        <div>
            <h1>Logout</h1>
        </div>
    );
}

function Dashboard() {
    return (
        <div>
            <Banner/>
        </div>
    )
}

export default Dashboard;