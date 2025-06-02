"use client";

import { useState, useEffect, useCallback } from "react";
import Card from "../components/events/event_card";
import styles from "./events.module.css";
import Pagination from "../components/pagination";
import SearchBar from "../components/search";
import Sidebar from "../components/events/side_bar";
import { useUser } from "../context/auth_context";
import { fetchEventsApi } from "../server_components/api";

interface Event {
  id: number;
  title: string;
  description: string;
  nb_places: number;
  price: number;
  date: string;
  cloture_billets: string;
  created_at: string;
  updated_at: string;
  nb_likes: number;
  nb_comments: number;
  profile: {
    id: number;
    first_name: string;
    last_name: string;
  };
  types: {
    id: number;
    type: string;
  }[];
  address: {
    id: number;
    city: string;
    zipcode: string;
    number: string;
    street: string;
    country: string;
  };
  pictures: {
    id: number;
    photo: string;
  }[];
}
export default function Events() {
  const [events, setEvents] = useState<Event[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  const [countResults, setCountResults] = useState(0);
  const [search, setSearch] = useState<string | null>(null);
  const [selectedTypes, setSelectedTypes] = useState<number[]>([]);
  const [dateAvant, setDateAvant] = useState<string | null>(null);
  const [dateApres, setDateApres] = useState<string | null>(null);
  const [city, setCity] = useState<string | null>(null);
  const [country, setCountry] = useState<string | null>(null);
  const [popular, setPopular] = useState<boolean>(true);
  const [recent, setRecent] = useState<boolean>(false);
  const limit = 5;

  const user = useUser();
  if (user){
    console.log(user)
  } else{
    console.log("pas connecté")
  }

  console.log(selectedTypes);

  const fetchData = useCallback(async () => {
    const offset = (currentPage - 1) * limit;
    let url = `/events?limit=${limit}&offset=${offset}`;
    if (selectedTypes.length !== 0){
      const typeParams = selectedTypes.map(id => `type_ids=${id}`).join("&");
      url += `&${typeParams}`;
    }

    if (search) {
      url += `&search=${encodeURIComponent(search)}`;
    }

    if (city) {
      url += `&city=${encodeURIComponent(city)}`;
    }

    if (country) {
      url += `&country=${encodeURIComponent(country)}`;
    }

    if (recent) {
      url += `&recent=${recent}`;
    }

    if (popular) {
      url += `&popularity=${popular}`;
    }

    if (dateAvant && /^\d{4}-\d{2}-\d{2}$/.test(dateAvant)) {
      url += `&date_avant=${dateAvant}`;
    }

    if (dateApres && /^\d{4}-\d{2}-\d{2}$/.test(dateApres)) {
      url += `&date_apres=${dateApres}`;
    }

    const data = await fetchEventsApi(url);

    setEvents(data.data);
    setTotalResults(data.total);
    setCountResults(data.count);
    setTotalPages(Math.ceil(data.total / limit));
  }, [currentPage, search, selectedTypes, dateAvant, dateApres, city, country, popular, recent]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    setCurrentPage(1);
  }, [search, selectedTypes, dateAvant, dateApres, city, country]);



  const selectTypes = (type_id: number) => {
        setSelectedTypes(prev => {
            if (prev.includes(type_id)) {
              return prev.filter(id => id !== type_id);
            } else {
              return [...prev, type_id];
            }
        });
    };

  const onDateAvantChange = (date) => {
    console.log(date);
    setDateAvant(date);
  }

  const onDateApresChange = (date) => {
    console.log(date);
    setDateApres(date);
  }

  const onCityChange = (city) => {
    setCity(city)
  }

  const onCountryChange = (country) => {
    setCountry(country)
  }

  const onPopularToggle = (popular) => {
    setPopular(popular)
  }

  const onRecentToggle = (recent) => {
    setRecent(recent)
  }

  return (
    <Sidebar
      onSelect={selectTypes}
      selectedTypes={selectedTypes}
      onDateAvantChange={onDateAvantChange}
      dateAvant={dateAvant}
      onDateApresChange={onDateApresChange}
      dateApres={dateApres}
      city={city}
      onCityChange={onCityChange}
      country={country}
      onCountryChange={onCountryChange}
      popular={popular}
      onPopularToggle={onPopularToggle}
      recent={recent}
      onRecentToggle={onRecentToggle}

    >
      <div className="p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 tracking-tight text-center">
          Événements
        </h1>

        <SearchBar
          onSearch={(term) => {
            setSearch(term === "" ? null : term);
            setCurrentPage(1);
          }}
          prop_type="évènement"
        />

        <p className={`${styles.resultNumber}`}>
          {countResults} résultats sur {totalResults}
        </p>

        <div className={`${styles.eventContainer} grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8`}>
          {events.map((event) => (
            <Card
              key={event.id}
              title={event.title}
              username={`${event.profile.first_name} ${event.profile.last_name}`}
              address={`${event.address.number}, ${event.address.street}, ${event.address.city}, ${event.address.country}`}
              price={event.price}
              nb_likes={event.nb_likes}
              description={event.description}
              pictureUrl={"/no_pic.jpg"}
              isLoggedIn={!!user}
              event_id={event.id}
              organizer_id={event.profile.id}
              types={event.types}
            />
          ))}
        </div>

        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={(page) => setCurrentPage(page)}
        />
      </div>
    </Sidebar>
  );
}
