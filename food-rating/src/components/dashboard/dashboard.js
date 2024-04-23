import './dashboard.css';

function Banner() {
    return (
        <div className="ban-cont">
            <h1 className="ban-header">Food Rating</h1>
        </div>
    );
}

function TopFoodItemsEntry() {
    return (
        <div className="tfi-entry">
            <p className='tfi-title'>5 Layer Burrito</p>
            <p className='tfi-rating'>4.4 Stars</p>
        </div>
    );
}

function TopFoodItems() {
    return (
        <div className="tfi-cont">
            <p className="tfi-header">Top Food Items</p>
            <div className="tfi-list">
                <TopFoodItemsEntry/>
                <TopFoodItemsEntry/>
                <TopFoodItemsEntry/>
                <TopFoodItemsEntry/>
                <TopFoodItemsEntry/>
                <TopFoodItemsEntry/>
                <TopFoodItemsEntry/>
            </div>
        </div>
    );
}

function TopCompaniesEntry() {
    return (
        <div className="tco-entry">
            <p className="tco-rating">4.4</p>
            <p className="tco-name">Taco Bell</p>
        </div>
    );
}

function TopCompanies() {
    return (
        <div className="tco-cont">
            <p className="tco-header">Top Companies</p>
            <div className="tco-list">
                <TopCompaniesEntry/>
                <TopCompaniesEntry/>
                <TopCompaniesEntry/>
                <TopCompaniesEntry/>
                <TopCompaniesEntry/>
                <TopCompaniesEntry/>
                <TopCompaniesEntry/>
                <TopCompaniesEntry/>
                <TopCompaniesEntry/>
                <TopCompaniesEntry/>
            </div>
        </div>
    );
}

function FoodEntriesControls() {
    return (
        <div className="fe-ctrl">
            <input type="text" placeholder="company"></input>
            <input type="text" placeholder="food"></input>
        </div>
    );
}

function FoodEntry() {
    return (
            <div className="fe-entry">
                <p className="fe-rating">4.4</p>
                <p className="fe-count">146</p>
                <p className="fe-name">Chalupa</p>
                <p className="fe-comp">Taco Bell</p>
            </div>
        );
}

function FoodEntries() {
    return (
        <div className="fe-cont">
            <p className="fe-header">Food Entries</p>
            <FoodEntriesControls/>
            <div>
                <div className="fe-bar">
                    <button>Rating</button>
                    <button>Num Ratings</button>
                    <button>Name</button>
                    <button>Company</button>
                </div>
                <div className="fe-list">
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                    <FoodEntry/>
                </div>
            </div>
        </div>
    );
}

function AddEntry() {
    return (
        <div className="add-cont">
            <button className="add-btn">Add</button>
        </div>
    );
}

function Logout() {
    return (
        <div className="log-cont">
            <button className="log-btn">Logout</button>
        </div>
    );
}

function Dashboard() {
    return (
        <div>
            <Banner/>
            <TopFoodItems/>
            <div className="sec-tables">
                <TopCompanies/>
                <FoodEntries/>
                <div className="sec-util">
                    <AddEntry/>
                    <Logout/>
                </div>
            </div>
        </div>
    )
}

export default Dashboard;