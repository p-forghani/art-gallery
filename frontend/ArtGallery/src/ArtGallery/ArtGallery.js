import React, { useState, useCallback, useEffect } from "react";
import ScrollLock from "react-scrolllock";
import { getCardById } from "../services/api";

import { Nav } from "./Nav/Nav";
import { Gallery } from "./Gallery/Gallery";
import { FloatingArrow } from "./FloatingArrow/FloatingArrow";
import { ZoomCardItem } from "./ZoomCardItem/ZoomCardItem";

import "./art-gallery.css";

export const ArtGallery = (props) => {
  const [lock, setLock] = useState(false);
  const [search, setSearch] = useState("");
  const [card, setCard] = useState([]);
  const [wide, setWide] = useState(false);

  useEffect(
    () => {
      if (props.windowWidth < 501) {
        console.log("narrow");
        setWide(false);
      } else {
        console.log("wide");
        setWide(true);
      }
    },
    [props.windowWidth] // Occurs when the state within is changing
  );

  // Recieve search data from Nav component, init search state
  const recieveNavSearchText = useCallback(
    (props) => {
      // Update searched text in the state
      setSearch(props);
    },
    [] //search
  );

  const recieveTagSearchText = useCallback(
    (props) => {
      // Update searched text in the state

      setLock(false);

      setSearch(props.toLowerCase());
    },
    [] //search
  );

  const recieveCardDetails = useCallback((propsChild) => {
    let cardId = propsChild.id;
    console.log("from recieveCardDetails", cardId);

    recieveCardFromDB(cardId);
  }, []);

  function recieveCardFromDB(cardId) {
    // Replace Firebase with our API service call
    const fetchCard = async () => {
      const cardData = await getCardById(cardId);
      setCard(cardData);
      setLock(true);
    };
    
    fetchCard();
  }

  return (
    <div id="ArtGallery" className="wide-art-gallery">
      <div
        className={
          lock
            ? wide
              ? "art-gallery-background avoid-clicks"
              : "art-gallery-background avoid-clicks no-scroll"
            : ""
        }
      >
        <Nav search={search} handleNavSearch={recieveNavSearchText} />
        <Gallery
          search={search}
          handleGalleryClickedCard={recieveCardDetails}
        />
        {wide && lock && <ScrollLock />}
      </div>

      {card === undefined || card.length === 0 || !lock ? (
        <FloatingArrow />
      ) : (
        <div className={wide ? "zoom-card-wide" : "zoom-card-narrow"}>
          <i
            className="fas fa-times exit-icon"
            onClick={() => setLock(false)}
          />
          <ZoomCardItem card={card} handleTagSearch={recieveTagSearchText} />
        </div>
      )}
    </div>
  );
};
